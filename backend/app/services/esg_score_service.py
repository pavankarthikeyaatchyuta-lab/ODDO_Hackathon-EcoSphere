from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.esg_score import DepartmentScore
from app.models.settings import ESGWeightSettings
from app.models.department import Department
from typing import List, Dict


def get_weights(db: Session) -> Dict[str, float]:
    settings = db.query(ESGWeightSettings).first()
    if not settings:
        return {"environmental": 40.0, "social": 30.0, "governance": 30.0}
    return {
        "environmental": settings.environmental_weight,
        "social": settings.social_weight,
        "governance": settings.governance_weight,
    }


def calculate_department_score(env: float, social: float, gov: float, weights: Dict) -> float:
    total_weight = weights["environmental"] + weights["social"] + weights["governance"]
    return round(
        (env * weights["environmental"] + social * weights["social"] + gov * weights["governance"]) / total_weight,
        2,
    )


def get_org_esg_score(db: Session) -> Dict:
    weights = get_weights(db)
    departments = db.query(Department).all()
    dept_scores = []
    for dept in departments:
        latest = (
            db.query(DepartmentScore)
            .filter(DepartmentScore.department_id == dept.id)
            .order_by(DepartmentScore.calculated_at.desc())
            .first()
        )
        if latest:
            dept_scores.append({
                "department_id": dept.id,
                "department_name": dept.name,
                "environmental_score": latest.environmental_score,
                "social_score": latest.social_score,
                "governance_score": latest.governance_score,
                "total_score": latest.total_score,
            })

    if not dept_scores:
        return {"org_score": 0, "department_scores": [], "weights": weights}

    org_score = round(sum(d["total_score"] for d in dept_scores) / len(dept_scores), 2)
    return {"org_score": org_score, "department_scores": dept_scores, "weights": weights}


def update_weights(db: Session, environmental: float, social: float, governance: float):
    if abs(environmental + social + governance - 100) > 0.01:
        raise ValueError("Weights must sum to 100")
    settings = db.query(ESGWeightSettings).first()
    if not settings:
        settings = ESGWeightSettings()
        db.add(settings)
    settings.environmental_weight = environmental
    settings.social_weight = social
    settings.governance_weight = governance
    db.commit()
    return settings
