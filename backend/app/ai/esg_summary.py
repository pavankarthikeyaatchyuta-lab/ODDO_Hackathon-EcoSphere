from sqlalchemy.orm import Session
from app.ai.gemini_client import ask
from app.models.esg_score import DepartmentScore
from app.models.department import Department


def generate_esg_summary(db: Session) -> str:
    scores = db.query(DepartmentScore).order_by(DepartmentScore.calculated_at.desc()).limit(20).all()
    if not scores:
        return "No ESG score data available yet to generate a summary."

    lines = []
    for s in scores:
        dept = db.query(Department).filter(Department.id == s.department_id).first()
        name = dept.name if dept else f"Dept {s.department_id}"
        lines.append(f"- {name}: E={s.environmental_score}, S={s.social_score}, G={s.governance_score}, Total={s.total_score}")

    prompt = f"""You are an ESG analyst. Based on the following department scores, write a concise executive summary (3-4 sentences) highlighting key strengths, areas of concern, and one actionable recommendation.

Department ESG Scores:
{chr(10).join(lines)}

Write the summary in plain English for a business audience."""

    return ask(prompt, fallback="ESG summary generation is temporarily unavailable.")
