from celery import Celery
import os
import time
import sqlite3

# RedisブローカーのURLを取得
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)

@app.task(name="tasks.evaluate_code")
def evaluate_code(user_code, submission_id):
    # 実際のコード評価ロジックをここに追加
    time.sleep(20)
    result = f"Evaluated code: {user_code}"
    # 提出IDを使用して結果を更新
    update_submission_result(submission_id, result)
    return result

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
