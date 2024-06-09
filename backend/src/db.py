import sqlite3
from typing import Optional, Literal

Status = Literal["WJ", "AC", "WA", "RE", "TLE", "MLE", "IE"]


def init_db() -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS submissions')

    # usersテーブルの作成
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # teamsテーブルの作成
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # team_membersテーブルの作成
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS team_members (
            user_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, team_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
        )
    """
    )

    # submissionsテーブルの作成
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            problem_name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            team_id INTEGER,
            code TEXT NOT NULL,
            status TEXT,
            execution_time REAL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pass_cases INTEGER DEFAULT 0
        )
    """
    )

    conn.commit()
    conn.close()


def add_user(username: str, email: str, password_hash: str) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    """,
        (username, email, password_hash),
    )
    conn.commit()
    conn.close()


def update_user(
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password_hash: Optional[str] = None,
) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    if username:
        c.execute(
            """
            UPDATE users
            SET username = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (username, user_id),
        )
    if email:
        c.execute(
            """
            UPDATE users
            SET email = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (email, user_id),
        )
    if password_hash:
        c.execute(
            """
            UPDATE users
            SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (password_hash, user_id),
        )
    conn.commit()
    conn.close()


def delete_user(user_id: int) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM users
        WHERE id = ?
    """,
        (user_id,),
    )
    conn.commit()
    conn.close()


def add_team(name: str) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO teams (name)
        VALUES (?)
    """,
        (name,),
    )
    conn.commit()
    conn.close()


def update_team(team_id: int, name: Optional[str] = None) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    if name:
        c.execute(
            """
            UPDATE teams
            SET name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (name, team_id),
        )
    conn.commit()
    conn.close()


def delete_team(team_id: int) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM teams
        WHERE id = ?
    """,
        (team_id,),
    )
    conn.commit()
    conn.close()


def add_submission(
    submission_id: str,
    problem_name: str,
    user_id: int,
    code: str,
    status: Status,
    execution_time: Optional[float] = None,
    team_id: Optional[int] = None,
    pass_cases: int = 0,
) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO submissions (id, problem_name, user_id, code, status, execution_time, team_id, pass_cases)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (submission_id, problem_name, user_id, code, status, execution_time, team_id, pass_cases),
    )
    conn.commit()
    conn.close()


def update_submission(submission_id: str, status: Optional[Status] = None, execution_time: Optional[float] = None, pass_cases: Optional[int] = None) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    if status:
        c.execute(
            """
            UPDATE submissions
            SET status = ?
            WHERE id = ?
        """,
            (status, submission_id),
        )
    if execution_time:
        c.execute(
            """
            UPDATE submissions
            SET execution_time = ?
            WHERE id = ?
        """,
            (execution_time, submission_id),
        )
    if pass_cases:
        c.execute(
            """
            UPDATE submissions
            SET pass_cases = ?
            WHERE id = ?
        """,
            (pass_cases, submission_id),
        )
    conn.commit()
    conn.close()

def get_submission(submission_id: str) -> dict:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        SELECT * FROM submissions
        WHERE id = ?
    """,
        (submission_id,),
    )
    submission = c.fetchone()
    conn.close()
    return {
        "id": submission[0],
        "problem_name": submission[1],
        "user_id": submission[2],
        "team_id": submission[3],
        "code": submission[4],
        "status": submission[5],
        "execution_time": submission[6],
        "submitted_at": submission[7],
        "pass_cases": submission[8],
    }


def delete_submission(submission_id: str) -> None:
    conn = sqlite3.connect("/app/data/database.db")
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM submissions
        WHERE id = ?
    """,
        (submission_id,),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
