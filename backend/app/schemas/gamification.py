from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.gamification import ChallengeStatus


class ChallengeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    xp_reward: int = 0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ChallengeUpdate(BaseModel):
    status: Optional[ChallengeStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None


class ChallengeOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    xp_reward: int
    status: ChallengeStatus
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    model_config = {"from_attributes": True}


class BadgeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    unlock_rule_type: str
    unlock_rule_value: int


class BadgeOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    unlock_rule_type: str
    unlock_rule_value: int
    created_at: datetime
    model_config = {"from_attributes": True}


class RewardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    xp_cost: int
    stock: int = 0


class RewardOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    xp_cost: int
    stock: int
    is_active: bool
    model_config = {"from_attributes": True}


class RedemptionOut(BaseModel):
    id: int
    reward_id: int
    user_id: int
    xp_spent: int
    redeemed_at: datetime
    model_config = {"from_attributes": True}
