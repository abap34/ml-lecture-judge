import sqlite3

def init_db():
    print("Initializing database...")
    # dbファイルが存在しない場合は作成して、テーブルを作成
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            problem TEXT,
            code TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_submission(username, problem, code, result):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO submissions (username, problem, code, result)
        VALUES (?, ?, ?, ?)
    ''', (username, problem, code, result))
    conn.commit()
    submission_id = c.lastrowid
    conn.close()
    return submission_id

def get_submissions():
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM submissions')
    submissions = c.fetchall()
    conn.close()
    return submissions

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


if __name__ == "__main__":
    init_db()