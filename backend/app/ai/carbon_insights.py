from sqlalchemy.orm import Session
from sqlalchemy import func
from app.ai.gemini_client import ask
from app.models.environmental import CarbonTransaction
from app.models.department import Department


def generate_carbon_insights(db: Session) -> str:
    results = (
        db.query(
            CarbonTransaction.department_id,
            func.sum(CarbonTransaction.co2_equivalent).label("total_co2"),
            func.count(CarbonTransaction.id).label("tx_count"),
        )
        .group_by(CarbonTransaction.department_id)
        .all()
    )

    if not results:
        return "No carbon transaction data available yet."

    total = sum(r.total_co2 for r in results)
    lines = []
    for r in results:
        dept = db.query(Department).filter(Department.id == r.department_id).first()
        name = dept.name if dept else f"Dept {r.department_id}"
        pct = round(r.total_co2 / total * 100, 1) if total else 0
        lines.append(f"- {name}: {r.total_co2:.2f} kg CO2 ({pct}% of total, {r.tx_count} transactions)")

    prompt = f"""You are a carbon footprint analyst. Analyze these department-level CO2 emissions and provide 3-4 bullet-point insights. Include which department emits most relative to others, any patterns, and one specific reduction recommendation.

Carbon Emissions by Department:
{chr(10).join(lines)}
Total emissions: {total:.2f} kg CO2"""

    return ask(prompt, fallback="Carbon insights are temporarily unavailable.")
