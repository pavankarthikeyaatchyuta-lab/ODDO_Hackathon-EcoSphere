from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.governance import (
    PolicyCreate, PolicyOut,
    AuditCreate, AuditUpdate, AuditOut,
    ComplianceIssueCreate, ComplianceIssueUpdate, ComplianceIssueOut,
)
from app.services import governance_service
from app.services.business_rules_service import flag_overdue_compliance

router = APIRouter(prefix="/api/governance", tags=["governance"])


@router.get("/policies", response_model=List[PolicyOut])
def list_policies(active_only: bool = False, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.get_policies(db, active_only)


@router.post("/policies", response_model=PolicyOut, status_code=201)
def create_policy(data: PolicyCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.create_policy(db, data)


@router.post("/policies/{policy_id}/acknowledge")
def acknowledge_policy(policy_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return governance_service.acknowledge_policy(db, policy_id, current_user.id)


@router.get("/audits", response_model=List[AuditOut])
def list_audits(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.get_audits(db)


@router.post("/audits", response_model=AuditOut, status_code=201)
def create_audit(data: AuditCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.create_audit(db, data)


@router.patch("/audits/{audit_id}", response_model=AuditOut)
def update_audit(audit_id: int, data: AuditUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.update_audit(db, audit_id, data)


@router.get("/compliance", response_model=List[ComplianceIssueOut])
def list_compliance(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.get_compliance_issues(db)


@router.post("/compliance", response_model=ComplianceIssueOut, status_code=201)
def create_compliance(data: ComplianceIssueCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.create_compliance_issue(db, data)


@router.patch("/compliance/{issue_id}", response_model=ComplianceIssueOut)
def update_compliance(issue_id: int, data: ComplianceIssueUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return governance_service.update_compliance_issue(db, issue_id, data)


@router.post("/compliance/check-overdue")
def check_overdue(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    count = flag_overdue_compliance(db)
    return {"flagged": count}
