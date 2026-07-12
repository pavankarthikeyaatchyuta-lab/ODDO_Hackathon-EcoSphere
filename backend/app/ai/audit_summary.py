from sqlalchemy.orm import Session
from app.ai.gemini_client import ask
from app.models.governance import Audit, ComplianceIssue, ComplianceStatus


def generate_audit_summary(db: Session) -> str:
    audits = db.query(Audit).order_by(Audit.scheduled_date.desc()).limit(10).all()
    open_issues = db.query(ComplianceIssue).filter(
        ComplianceIssue.status.in_([ComplianceStatus.open, ComplianceStatus.overdue])
    ).count()

    if not audits:
        return "No audit data available to summarize."

    audit_lines = [
        f"- {a.title}: status={a.status.value}, score={a.score or 'N/A'}"
        for a in audits
    ]

    prompt = f"""You are a governance compliance analyst. Summarize the following audit findings in 3-4 sentences. Highlight compliance posture, any red flags, and one priority action item.

Recent Audits:
{chr(10).join(audit_lines)}
Open/Overdue Compliance Issues: {open_issues}"""

    return ask(prompt, fallback="Audit summary is temporarily unavailable.")
