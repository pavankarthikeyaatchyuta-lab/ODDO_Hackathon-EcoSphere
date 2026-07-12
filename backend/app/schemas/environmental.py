from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.models.environmental import EmissionSourceType, GoalStatus


class EmissionFactorCreate(BaseModel):
    name: str
    source_type: EmissionSourceType
    factor_value: float
    unit: str
    description: Optional[str] = None

    @field_validator("factor_value")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("factor_value must be positive")
        return v


class EmissionFactorOut(BaseModel):
    id: int
    name: str
    source_type: EmissionSourceType
    factor_value: float
    unit: str
    description: Optional[str]
    created_at: datetime
    model_config = {"from_attributes": True}


class CarbonTransactionCreate(BaseModel):
    department_id: int
    emission_factor_id: Optional[int] = None
    source_type: EmissionSourceType
    quantity: float
    description: Optional[str] = None

    @field_validator("quantity")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("quantity must be positive")
        return v


class CarbonTransactionOut(BaseModel):
    id: int
    department_id: int
    emission_factor_id: Optional[int]
    source_type: EmissionSourceType
    quantity: float
    co2_equivalent: float
    description: Optional[str]
    auto_generated: bool
    date: datetime
    model_config = {"from_attributes": True}


class EnvironmentalGoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_value: float
    unit: str
    target_date: datetime


class EnvironmentalGoalUpdate(BaseModel):
    current_value: Optional[float] = None
    status: Optional[GoalStatus] = None


class EnvironmentalGoalOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    target_value: float
    current_value: float
    unit: str
    status: GoalStatus
    target_date: datetime
    created_at: datetime
    model_config = {"from_attributes": True}
