from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.models.governance import ComplianceStatus, AuditStatus


class PolicyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    effective_date: datetime
    review_date: Optional[datetime] = None
    document_url: Optional[str] = None


class PolicyOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    effective_date: datetime
    review_date: Optional[datetime]
    is_active: bool
    document_url: Optional[str]
    created_at: datetime
    model_config = {"from_attributes": True}


class AuditCreate(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    auditor_id: Optional[int] = None
    scheduled_date: datetime


class AuditUpdate(BaseModel):
    status: Optional[AuditStatus] = None
    score: Optional[float] = None
    findings: Optional[str] = None
    completed_date: Optional[datetime] = None


class AuditOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    department_id: Optional[int]
    auditor_id: Optional[int]
    status: AuditStatus
    score: Optional[float]
    findings: Optional[str]
    scheduled_date: datetime
    completed_date: Optional[datetime]
    created_at: datetime
    model_config = {"from_attributes": True}


class ComplianceIssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    audit_id: Optional[int] = None
    owner_id: int
    severity: Optional[str] = None
    due_date: datetime

    @field_validator("owner_id")
    @classmethod
    def owner_required(cls, v):
        if v is None:
            raise ValueError("owner_id is required for compliance issues")
        return v


class ComplianceIssueUpdate(BaseModel):
    status: Optional[ComplianceStatus] = None
    resolved_at: Optional[datetime] = None


class ComplianceIssueOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    audit_id: Optional[int]
    owner_id: int
    status: ComplianceStatus
    severity: Optional[str]
    due_date: datetime
    resolved_at: Optional[datetime]
    created_at: datetime
    model_config = {"from_attributes": True}
