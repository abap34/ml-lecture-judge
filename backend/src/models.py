from datetime import datetime
from typing import Literal, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

Status = Literal["WJ", "AC", "WA", "RE", "TLE", "MLE", "IE"]


def jst_now():
    return datetime.now(ZoneInfo("Asia/Tokyo"))


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, default=jst_now)
    icon_url = Column(String, nullable=True)


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=jst_now)
    updated_at = Column(TIMESTAMP, default=jst_now)


class TeamMember(Base):
    __tablename__ = "team_members"
    user_id = Column(String, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    joined_at = Column(TIMESTAMP, default=jst_now)


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(String, primary_key=True, index=True)
    problem_name = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    team_id = Column(Integer, nullable=True)
    code = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    execution_time = Column(Float, nullable=True)
    submitted_at = Column(TIMESTAMP, default=jst_now)
    pass_cases = Column(Integer, default=0)
    get_points = Column(Integer, default=0)


class CodeSubmission(BaseModel):
    code: str
    userid: str
    problem_name: str


class ProblemSummary(BaseModel):
    name: str
    title: str
    section: int
    point: int

JudgeQueueStatus = Literal["Pending", "Running", "Completed"]


class SubmissionResult(BaseModel):
    status: JudgeQueueStatus
    result: dict


class ProblemDetail(BaseModel):
    settings: dict
    description: str

    class Config:
        orm_mode = True

class UserLeaderBoardRow(BaseModel):
    id: str
    rank: int
    icon_url: str
    total_points: int
    total_submissions: int

class TeamLeaderBoardRow(BaseModel):
    id: int
    name: str
    total_points: int
    total_submissions: int
    created_at: datetime
    updated_at: datetime
    members: list[str]