from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import yaml
import glob

import uvicorn


from judge.tasks import evaluate_code


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



@app.post("/submit")
async def submit_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    submission_time = datetime.now().isoformat()
    task = evaluate_code.delay(code, submission_time)
    return {"task_id": task.id, "status": "Submitted"}

@app.get("/result/{task_id}")
def get_result(task_id: str):
    task = evaluate_code.AsyncResult(task_id)
    if task.ready():
        return {"status": "Completed", "result": task.get()}
    else:
        return {"status": "Pending"}
    
# 全部の問題名を返す
@app.get("/problems")
def get_problems():
    problems = glob.glob("static/problems/*")
    # helper.py は除外してディレクトリ名だけを返す
    problems = [problem.split("/")[-1] for problem in problems if problem != "static/problems/helper.py"]
    # タイトルもとる
    problems = [{"name": problem, "title": yaml.safe_load(open(f"static/problems/{problem}/problem.yaml"))["summary"]["title"]} for problem in problems]
    return {
        "problems": [problem for problem in problems]
    }

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
