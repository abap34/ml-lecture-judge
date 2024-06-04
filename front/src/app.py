import streamlit as st
from celery import Celery
import os
from db import init_db, add_submission, get_submissions

# Celeryクライアントを設定
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
celery_app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

st.title("ml-lecture-evaluation")
user_code = st.text_area("Input your code here", height=200)

if st.button("submit", key="submit"):
    st.write("Submitting...")
    submission_id = add_submission("user", "problem1", user_code, "WJ")
    task = celery_app.send_task('tasks.evaluate_code', args=[user_code, submission_id])
    
    st.write("Your code has been submitted for evaluation. Please check back later for the result.")

# 保存された投稿結果を表示
st.subheader("Submission History")
submissions = get_submissions()
for submission in submissions:
    st.write(f"Username: {submission[1]}")
    st.write(f"Problem: {submission[2]}")
    st.write(f"Code: {submission[3]}")
    st.write(f"Result: {submission[4]}")
    st.write("---")
