from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models import CodeSubmission, ProblemSummary, SubmissionResult, ProblemDetail
from db import SessionLocal, init_db, add_submission, update_submission, get_submission
from judge.tasks import evaluate_code
import yaml
import glob
import uvicorn
from typing import List, Dict, Optional

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
    inputs = glob.glob(f"static/problems/{problem_name}/in/*.in")
    testcases = [
        {
            "input": open(input_file).read(),
            "output": open(input_file.replace("/in/", "/out/").replace(".in", ".out")).read(),
        }
        for input_file in inputs
    ]
    return testcases

def get_constraints(problem_name: str) -> Dict[str, any]:
    with open(f"static/problems/{problem_name}/problem.yaml") as f:
        problem = yaml.safe_load(f)
    return problem["constraints"]

@app.post("/submit/{problem_name}")
async def submit_code(request: CodeSubmission, db: Session = Depends(get_db)):
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
            request.code, get_all_testcases(request.problem_name), timelimit, memorylimit
        )

    add_submission(db, task.id, request.problem_name, request.userid, request.code, "WJ", execution_time=None, team_id=None)
    return {"task_id": task.id, "status": "Submitted"}

@app.get("/reset_db/are_you_sure")
def reset_db():
    init_db()
    return {"status": "OK"}

@app.get("/result/{task_id}", response_model=SubmissionResult)
def get_result(task_id: str, db: Session = Depends(get_db)):
    task = evaluate_code.AsyncResult(task_id)
    if task.ready():
        result = task.get()
        update_submission(db, task_id, status=result.status, execution_time=result.time, pass_cases=result.pass_cases)
        try:
            submit = get_submission(db, task_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Submission not found")
        return submit
    else:
        return {
            "problem_name": "",
            "status": "Pending",
            "execution_time": 0,
            "code": "",
            "passed_cases": 0,
            "n_testcases": 0,
            "submitted_at": datetime.now(),
        }

@app.get("/problems", response_model=List[ProblemSummary])
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
            "title": yaml.safe_load(open(f"static/problems/{problem}/problem.yaml"))["summary"]["title"],
        }
        for problem in problems
    ]
    return problems

@app.get("/problems/{problem_name}", response_model=ProblemDetail)
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
