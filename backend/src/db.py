from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import NoResultFound
from models import Base, Submission
from typing import Optional

DATABASE_URL = "sqlite:///./data/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def add_submission(
    db: Session, submission_id: str, problem_name: str, user_id: int, code: str, status: str,
    execution_time: Optional[float] = None, team_id: Optional[int] = None, pass_cases: int = 0
) -> Submission:
    submission = Submission(
        id=submission_id,
        problem_name=problem_name,
        user_id=user_id,
        code=code,
        status=status,
        execution_time=execution_time,
        team_id=team_id,
        pass_cases=pass_cases
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

def update_submission(
    db: Session, submission_id: str, status: Optional[str] = None,
    execution_time: Optional[float] = None, pass_cases: Optional[int] = None
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise NoResultFound(f"No submission found with id: {submission_id}")
    if status:
        submission.status = status
    if execution_time is not None:
        submission.execution_time = execution_time
    if pass_cases is not None:
        submission.pass_cases = pass_cases
    db.commit()
    db.refresh(submission)

def get_submission(db: Session, submission_id: str) -> Submission:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise NoResultFound(f"No submission found with id: {submission_id}")
    return submission
