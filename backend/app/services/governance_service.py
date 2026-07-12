from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.governance import Policy, PolicyAcknowledgement, Audit, ComplianceIssue
from app.schemas.governance import (
    PolicyCreate, AuditCreate, AuditUpdate,
    ComplianceIssueCreate, ComplianceIssueUpdate
)
from app.models.notification import NotificationType
from app.services.notification_service import create_notification


def create_policy(db: Session, data: PolicyCreate) -> Policy:
    policy = Policy(**data.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def get_policies(db: Session, active_only: bool = False):
    q = db.query(Policy)
    if active_only:
        q = q.filter(Policy.is_active == True)
    return q.order_by(Policy.created_at.desc()).all()


def acknowledge_policy(db: Session, policy_id: int, user_id: int) -> PolicyAcknowledgement:
    existing = db.query(PolicyAcknowledgement).filter(
        PolicyAcknowledgement.policy_id == policy_id,
        PolicyAcknowledgement.user_id == user_id
    ).first()
    if existing:
        return existing
    ack = PolicyAcknowledgement(policy_id=policy_id, user_id=user_id)
    db.add(ack)
    db.commit()
    db.refresh(ack)
    return ack


def create_audit(db: Session, data: AuditCreate) -> Audit:
    audit = Audit(**data.model_dump())
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def update_audit(db: Session, audit_id: int, data: AuditUpdate) -> Audit:
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(audit, k, v)
    db.commit()
    db.refresh(audit)
    return audit


def get_audits(db: Session):
    return db.query(Audit).order_by(Audit.scheduled_date.desc()).all()


def create_compliance_issue(db: Session, data: ComplianceIssueCreate) -> ComplianceIssue:
    issue = ComplianceIssue(**data.model_dump())
    db.add(issue)
    db.commit()
    db.flush()
    create_notification(
        db, data.owner_id,
        NotificationType.compliance_issue,
        "Compliance Issue Assigned",
        f"You have been assigned compliance issue: {data.title}. Due: {data.due_date.strftime('%Y-%m-%d')}"
    )
    db.commit()
    db.refresh(issue)
    return issue


def update_compliance_issue(db: Session, issue_id: int, data: ComplianceIssueUpdate) -> ComplianceIssue:
    issue = db.query(ComplianceIssue).filter(ComplianceIssue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Compliance issue not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(issue, k, v)
    db.commit()
    db.refresh(issue)
    return issue


def get_compliance_issues(db: Session):
    return db.query(ComplianceIssue).order_by(ComplianceIssue.created_at.desc()).all()
