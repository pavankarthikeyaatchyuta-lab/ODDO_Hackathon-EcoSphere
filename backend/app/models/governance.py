from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ComplianceStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    overdue = "overdue"


class AuditStatus(str, enum.Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    effective_date = Column(DateTime(timezone=True), nullable=False)
    review_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    document_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    acknowledgements = relationship("PolicyAcknowledgement", back_populates="policy")


class PolicyAcknowledgement(Base):
    __tablename__ = "policy_acknowledgements"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), server_default=func.now())

    policy = relationship("Policy", back_populates="acknowledgements")
    user = relationship("User", back_populates="policy_acknowledgements")


class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    auditor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(AuditStatus), default=AuditStatus.planned)
    score = Column(Float)
    findings = Column(Text)
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    completed_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    department = relationship("Department", back_populates="audits")
    auditor = relationship("User")
    compliance_issues = relationship("ComplianceIssue", back_populates="audit")


class ComplianceIssue(Base):
    __tablename__ = "compliance_issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.open)
    severity = Column(String)
    due_date = Column(DateTime(timezone=True), nullable=False)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    audit = relationship("Audit", back_populates="compliance_issues")
    owner = relationship("User")
