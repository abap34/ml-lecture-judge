from fastapi import APIRouter, Depends
from db import add_submission, get_submissions
from judge.tasks import celery_app

router = APIRouter()

@router.post("/submit")
def submit_code(user_code: str):
    submission_id = add_submission("user", "problem1", user_code, "WJ")
    celery_app.send_task("tasks.evaluate_code", args=[user_code, submission_id])
    return {"status": "success", "submission_id": submission_id}

@router.get("/submissions")
def list_submissions():
    submissions = get_submissions()
    return submissions
