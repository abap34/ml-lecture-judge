from celery import Celery
import os
import time
import sqlite3

# RedisブローカーのURLを取得
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

@app.task(name="tasks.evaluate_code")
def evaluate_code(code, submission_time):
    print("Evaluating code...")
    time.sleep(5)
    print("Code evaluated.")
    return eval(code), submission_time

def update_submission_result(submission_id, result):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        UPDATE submissions
        SET result = ?
        WHERE id = ?
    ''', (result, submission_id))
    conn.commit()
    conn.close()
