from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yaml
import glob
import uvicorn
from judge.tasks import evaluate_code
import sqlite3
from db import add_submission, update_submission, get_submission, init_db


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


def n_testcases(problem_name: str) -> int:
    inputs = glob.glob(f"static/problems/{problem_name}/in/*.in")
    return len(inputs)


def get_all_testcases(problem_name: str) -> list[tuple[str, str]]:
    inputs = glob.glob(f"static/problems/{problem_name}/in/*.in")
    outputs = glob.glob(f"static/problems/{problem_name}/out/*.out")
    testcases = [
        (open(input_file).read(), open(output_file).read())
        for input_file, output_file in zip(inputs, outputs)
    ]
    return testcases


def get_constraints(problem_name: str) -> dict:
    with open(f"static/problems/{problem_name}/problem.yaml") as f:
        problem = yaml.safe_load(f)
    return problem["constraints"]


@app.post("/submit/{problem_name}")
async def submit_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    username = data.get("userid", "")
    problem_name = data.get("problem_name", "")
    # 制約取得
    constraints = get_constraints(problem_name)
    timelimit = constraints["time"]
    memorylimit = constraints["memory"]

    task = evaluate_code.delay(
        code, get_all_testcases(problem_name), timelimit, memorylimit
    )
    # 投稿した瞬間は WJ
    add_submission(
        task.id, problem_name, username, code, "WJ", execution_time=None, team_id=None
    )
    return {"task_id": task.id, "status": "Submitted"}


# 注意！！！！！！　dbのすべてをリセットするエンドポイントが必要
@app.get("/reset_db/are_you_sure")
def reset_db():
    c = sqlite3.connect("data/database.db")
    # すべてのテーブルを削除
    c.execute("DROP TABLE submissions")
    c.execute("DROP TABLE users")
    c.execute("DROP TABLE teams")
    c.commit()
    c.close()
    # テーブルを再作成
    init_db()
    return {"status": "OK"}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    task = evaluate_code.AsyncResult(task_id)
    if task.ready():
        # 考え直した方がいいかも ?
        # -> このタイミングで db 更新
        update_submission(task_id, task.get()["status"], task.get()["time"], task.get()["pass_cases"])
        submit = get_submission(task_id)
        return {
            "status": "Completed",
            "result": {
                "problem_name": submit["problem_name"],
                "status": submit["status"],
                "execution_time": submit["execution_time"],
                "code": submit["code"],
                "passed_cases": submit["pass_cases"],
                "n_testcases": n_testcases(submit["problem_name"]),
                "submitted_at": submit["submitted_at"],
            },
        }
    else:
        return {"status": "Pending"}


# 全部の問題名を返す
@app.get("/problems")
def get_problems():
    problems = glob.glob("static/problems/*")
    # helper.py は除外してディレクトリ名だけを返す
    problems = [
        problem.split("/")[-1]
        for problem in problems
        if problem != "static/problems/helper.py"
    ]
    # タイトルもとる
    problems = [
        {
            "name": problem,
            "title": yaml.safe_load(open(f"static/problems/{problem}/problem.yaml"))[
                "summary"
            ]["title"],
        }
        for problem in problems
    ]
    return {"problems": [problem for problem in problems]}


# static/problems/{problem} 以下の内容を返す
# 返すもの: problem.yaml description.md
@app.get("/problems/{problem_name}")
def get_problem(problem_name: str):
    with open(f"static/problems/{problem_name}/problem.yaml") as f:
        problem = yaml.safe_load(f)
    with open(f"static/problems/{problem_name}/description.md") as f:
        description = f.read()
    return {"problem": problem, "description": description}


@app.get("/jobs")
def get_jobs():
    return evaluate_code.control.inspect().active()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
