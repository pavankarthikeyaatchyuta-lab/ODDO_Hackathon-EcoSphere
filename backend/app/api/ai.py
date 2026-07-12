from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai import esg_summary, carbon_insights, audit_summary, policy_explainer

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.get("/esg-summary")
def ai_esg_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return {"result": esg_summary.generate_esg_summary(db)}


@router.get("/carbon-insights")
def ai_carbon_insights(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return {"result": carbon_insights.generate_carbon_insights(db)}


@router.get("/audit-summary")
def ai_audit_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return {"result": audit_summary.generate_audit_summary(db)}


@router.get("/policy-explainer/{policy_id}")
def ai_policy_explainer(policy_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return {"result": policy_explainer.explain_policy(db, policy_id)}
