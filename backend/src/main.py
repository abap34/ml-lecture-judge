import base64
import glob
import json
import os
from datetime import datetime
from typing import Dict, List

import uvicorn
import yaml
from authlib.integrations.base_client.errors import OAuthError
from authlib.integrations.starlette_client import OAuth
from db import SessionLocal, add_submission, get_submission, init_db, update_submission
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from judge.tasks import evaluate_code
from models import CodeSubmission, ProblemDetail, ProblemSummary, SubmissionResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

oauth = OAuth()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://q.trap.jp/api/v3/oauth2/authorize",
    tokenUrl="https://q.trap.jp/api/v3/oauth2/token",
)

oauth.register(
    name="traq",
    client_id=os.getenv("TRAQ_CLIENT_ID"),
    client_secret=os.getenv("TRAQ_CLIENT_SECRET"),
    server_metadata_url="https://q.trap.jp/api/v3/oauth2/oidc/discovery",
)


client_id = os.getenv("TRAQ_CLIENT_ID")
client_secret = os.getenv("TRAQ_CLIENT_SECRET")
secret_key = os.getenv("SECRET_KEY")

if not all([client_id, client_secret, secret_key]):
    for key in ["TRAQ_CLIENT_ID", "TRAQ_CLIENT_SECRET", "SECRET_KEY"]:
        if not os.getenv(key):
            raise ValueError(f"{key} is not set")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def n_testcases(problem_name: str) -> int:
    inputs = glob.glob(f"static/problems/{problem_name}/in/*.in")
    return len(inputs)


def get_all_testcases(problem_name: str) -> List[Dict[str, str]]:
    inputs = sorted(glob.glob(f"static/problems/{problem_name}/in/*.in"))
    testcases = [
        {
            "input": open(input_file).read(),
            "output": open(
                input_file.replace("/in/", "/out/").replace(".in", ".out")
            ).read(),
        }
        for input_file in inputs
    ]
    return testcases


def get_constraints(problem_name: str) -> Dict[str, any]:
    with open(f"static/problems/{problem_name}/problem.yaml") as f:
        problem = yaml.safe_load(f)
    return problem["constraints"]


@app.get("/")
def read_root():
    return {"Hello": "?"}


def get_user_name(token: str) -> str:
    payload = token.split(".")[1]
    payload += "=" * ((4 - len(payload) % 4) % 4)
    return json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))["name"]


@app.get("/login_status")
async def login_status(request: Request):
    token = request.session.get("id_token")
    if token:
        return {"logged_in": True}
    return {"logged_in": False}


@app.get("/userinfo", dependencies=[Depends(oauth2_scheme)])
async def get_user_info(request: Request):
    token = request.session.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        userinfo = json.loads(base64.b64decode(token["id_token"].split(".")[1] + "=="))
        return {"userinfo": userinfo}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=400, detail=f"Token decoding error: {str(e)}")


@app.get("/login")
async def login(request: Request):
    return await oauth.traq.authorize_redirect(
        request, "http://localhost:8000/callback"
    )


@app.route("/callback")
async def auth(request: Request):
    try:
        token = await oauth.traq.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=401, detail="L133: " + str(e))

    request.session["id_token"] = token["id_token"]

    return RedirectResponse(url="http://localhost:3000/")


@app.post("/submit/{problem_name}")
async def submit_code(
    request: CodeSubmission,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    constraints = get_constraints(request.problem_name)
    timelimit = constraints["time"]
    memorylimit = constraints["memory"]
    error_judge = constraints.get("error_judge", False)

    if error_judge:
        abs_error = float(constraints.get("absolute_error", None))
        rel_error = float(constraints.get("relative_error", None))

        task = evaluate_code.delay(
            request.code,
            get_all_testcases(request.problem_name),
            timelimit,
            memorylimit,
            error_judge,
            abs_error,
            rel_error,
        )
    else:
        task = evaluate_code.delay(
            request.code,
            get_all_testcases(request.problem_name),
            timelimit,
            memorylimit,
        )

    add_submission(
        db,
        task.id,
        request.problem_name,
        request.userid,
        request.code,
        "WJ",
        execution_time=None,
        team_id=None,
    )
    return {"task_id": task.id, "status": "Submitted"}


@app.get("/reset_db/are_you_sure", dependencies=[Depends(oauth2_scheme)])
def reset_db():
    init_db()
    return {"status": "OK"}


@app.get(
    "/result/{task_id}",
    response_model=SubmissionResult,
    dependencies=[Depends(oauth2_scheme)],
)
def get_result(task_id: str, db: Session = Depends(get_db)):
    task = evaluate_code.AsyncResult(task_id)
    if task.ready():
        result = task.get()

        update_submission(
            db,
            task_id,
            status=result["status"],
            execution_time=result["time"],
            pass_cases=result["pass_cases"],
        )
        try:
            submit = get_submission(db, task_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Submission not found")
        return {
            "status": "Completed",
            "result": {
                "problem_name": submit.problem_name,
                "status": submit.status,
                "execution_time": submit.execution_time,
                "code": submit.code,
                "passed_cases": submit.pass_cases,
                "n_testcases": n_testcases(submit.problem_name),
                "submitted_at": submit.submitted_at,
            },
        }
    else:
        return {"status": "Pending", "result": {}}


@app.get(
    "/problems",
    response_model=List[ProblemSummary],
    dependencies=[Depends(oauth2_scheme)],
)
def get_problems():
    problems = glob.glob("static/problems/*")
    problems = [
        problem.split("/")[-1]
        for problem in problems
        if problem != "static/problems/helper.py"
    ]
    problems = [
        {
            "name": problem,
            "title": yaml.safe_load(open(f"static/problems/{problem}/problem.yaml"))[
                "summary"
            ]["title"],
        }
        for problem in problems
    ]
    return problems


@app.get(
    "/problems/{problem_name}",
    response_model=ProblemDetail,
    dependencies=[Depends(oauth2_scheme)],
)
def get_problem(problem_name: str):
    try:
        with open(f"static/problems/{problem_name}/problem.yaml") as f:
            problem = yaml.safe_load(f)
        with open(f"static/problems/{problem_name}/description.md") as f:
            description = f.read()
        return {"settings": problem, "description": description}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Problem not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
