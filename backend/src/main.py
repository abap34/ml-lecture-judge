from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{name}")
def read_item(name: str):
    return {"Hello": name}


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
    
@app.get("/jobs")
def get_jobs():
    return evaluate_code.control.inspect().active()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
