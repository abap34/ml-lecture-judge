import datetime
from typing import Optional

from models import Base, Submission, Team, TeamLeaderBoardRow, User, UserLeaderBoardRow
from sqlalchemy import asc, create_engine, desc, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "sqlite:///./data/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def add_submission(
    db: Session,
    submission_id: str,
    problem_name: str,
    user_id: int,
    code: str,
    status: str = "WJ",
    execution_time: Optional[float] = None,
    team_id: Optional[int] = None,
    pass_cases: int = 0,
    get_points: int = 0,
) -> Submission:
    submission = Submission(
        id=submission_id,
        problem_name=problem_name,
        user_id=user_id,
        code=code,
        status=status,
        execution_time=execution_time,
        team_id=team_id,
        pass_cases=pass_cases,
        get_points=get_points,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)


def update_submission(
    db: Session,
    submission_id: str,
    status: Optional[str] = None,
    execution_time: Optional[float] = None,
    pass_cases: Optional[int] = None,
    get_points: Optional[int] = None,
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
    if get_points is not None:
        submission.get_points = get_points
    db.commit()
    db.refresh(submission)


def get_submission(db: Session, submission_id: str) -> Submission:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise NoResultFound(f"No submission found with id: {submission_id}")
    return submission


def add_user(db: Session, id: str, icon_url: Optional[str] = None, duplicate_ok: bool = False) -> None:
    user = User(id=id, icon_url=icon_url)
    if not duplicate_ok:
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # いたら何もしない
        if db.query(User).filter(User.id == id).first() is None:
            db.add(user)
            db.commit()
            db.refresh(user)



def calculate_user_scores(db: Session) -> list[UserLeaderBoardRow]:
    results = (
        db.query(
            Submission.user_id,
            User.id,
            User.icon_url,
            func.sum(Submission.get_points).label("total_score"),
            func.count(Submission.id).label("total_submissions"),
        )
        .join(User, User.id == Submission.user_id)
        .filter(Submission.status == "AC")
        .group_by(Submission.user_id, User.id, User.icon_url)
        .order_by(desc("total_score"), asc("total_submissions"))
        .all()
    )

    print(results)

    return [
        UserLeaderBoardRow(
            id=user_id,
            icon_url=icon_url,
            total_points=total_score,
            total_submissions=total_submissions,
        )
        for user_id, user_id, icon_url, total_score, total_submissions in results
    ]


def calculate_team_scores(db: Session) -> list[TeamLeaderBoardRow]:
    results = (
        db.query(
            Submission.team_id,
            Team.name,
            func.sum(Submission.get_points).label("total_score"),
            func.count(Submission.id).label("total_submissions"),
        )
        .join(Team, Team.id == Submission.team_id)
        .filter(Submission.status == "AC")
        .group_by(Submission.team_id, Team.name)
        .order_by(desc("total_score"), asc("total_submissions"))
        .all()
    )

    return [
        TeamLeaderBoardRow(
            id=team_id,
            name=name,
            total_points=total_score,
            total_submissions=total_submissions,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            members=[],
        )
        for team_id, name, total_score, total_submissions in results
    ]
