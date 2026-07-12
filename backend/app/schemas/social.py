from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.social import ParticipationStatus


class CategoryCreate(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    type: Optional[str]
    description: Optional[str]
    model_config = {"from_attributes": True}


class CSRActivityCreate(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: int
    category_id: Optional[int] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    max_participants: Optional[int] = None
    xp_reward: int = 0


class CSRActivityOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    department_id: int
    category_id: Optional[int]
    start_date: datetime
    end_date: Optional[datetime]
    max_participants: Optional[int]
    xp_reward: int
    created_at: datetime
    model_config = {"from_attributes": True}


class ParticipationCreate(BaseModel):
    activity_id: int
    notes: Optional[str] = None


class ParticipationApprove(BaseModel):
    status: ParticipationStatus
    notes: Optional[str] = None


class ParticipationOut(BaseModel):
    id: int
    activity_id: int
    user_id: int
    status: ParticipationStatus
    evidence_file: Optional[str]
    notes: Optional[str]
    submitted_at: datetime
    reviewed_at: Optional[datetime]
    model_config = {"from_attributes": True}


class TrainingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    hours: float
    participants_count: int = 0
    completed_at: Optional[datetime] = None


class TrainingOut(BaseModel):
    id: int
    title: str
    hours: float
    participants_count: int
    completed_at: Optional[datetime]
    created_at: datetime
    model_config = {"from_attributes": True}
