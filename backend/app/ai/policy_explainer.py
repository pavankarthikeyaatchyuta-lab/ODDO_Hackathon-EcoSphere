from sqlalchemy.orm import Session
from app.ai.gemini_client import ask
from app.models.governance import Policy


def explain_policy(db: Session, policy_id: int) -> str:
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        return "Policy not found."

    prompt = f"""Explain the following company policy in plain, simple English for an employee who is not familiar with legal language. Keep it to 2-3 short paragraphs.

Policy title: {policy.title}
Policy description: {policy.description or 'No description provided.'}
Category: {policy.category or 'General'}
Effective date: {policy.effective_date}"""

    return ask(prompt, fallback="Policy explanation is temporarily unavailable.")
