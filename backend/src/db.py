import sqlite3

def init_db():
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()

    # usersテーブルの作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # teamsテーブルの作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # team_membersテーブルの作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            user_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, team_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
        )
    ''')

    # submissionsテーブルの作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            team_id INTEGER,
            code TEXT NOT NULL,
            status TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_user(username, email, password_hash):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    ''', (username, email, password_hash))
    conn.commit()
    conn.close()

def update_user(user_id, username=None, email=None, password_hash=None):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    if username:
        c.execute('''
            UPDATE users
            SET username = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (username, user_id))
    if email:
        c.execute('''
            UPDATE users
            SET email = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (email, user_id))
    if password_hash:
        c.execute('''
            UPDATE users
            SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (password_hash, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM users
        WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def add_team(name):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO teams (name)
        VALUES (?)
    ''', (name,))
    conn.commit()
    conn.close()

def update_team(team_id, name=None):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    if name:
        c.execute('''
            UPDATE teams
            SET name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, team_id))
    conn.commit()
    conn.close()

def delete_team(team_id):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM teams
        WHERE id = ?
    ''', (team_id,))
    conn.commit()
    conn.close()

def add_submission(problem_id, user_id, code, status, team_id=None):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO submissions (problem_id, user_id, code, status, team_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (problem_id, user_id, code, status, team_id))
    conn.commit()
    conn.close()

def update_submission(submission_id, status=None):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    if status:
        c.execute('''
            UPDATE submissions
            SET status = ?, submitted_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, submission_id))
    conn.commit()
    conn.close()

def delete_submission(submission_id):
    conn = sqlite3.connect('/app/data/database.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM submissions
        WHERE id = ?
    ''', (submission_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
