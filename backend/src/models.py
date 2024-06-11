from datetime import datetime
from typing import Literal, Optional
from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

Status = Literal["WJ", "AC", "WA", "RE", "TLE", "MLE", "IE"]


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)


class TeamMember(Base):
    __tablename__ = "team_members"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), primary_key=True)
    joined_at = Column(TIMESTAMP, default=datetime.utcnow)


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(String, primary_key=True, index=True)
    problem_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    code = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    execution_time = Column(Float, nullable=True)
    submitted_at = Column(TIMESTAMP, default=datetime.utcnow)
    pass_cases = Column(Integer, default=0)


class CodeSubmission(BaseModel):
    code: str
    userid: str
    problem_name: str


class ProblemSummary(BaseModel):
    name: str
    title: str


class SubmissionResult(BaseModel):
    problem_name: str
    status: str
    execution_time: Optional[float]
    code: str
    passed_cases: int
    n_testcases: int
    submitted_at: datetime

    class Config:
        orm_mode = True
