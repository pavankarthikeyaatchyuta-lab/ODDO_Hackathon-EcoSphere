from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict


def get_activity_feed(db: Session, limit: int = 20, offset: int = 0) -> List[Dict]:
    events = []

    from app.models.gamification import BadgeAward, RewardRedemption
    from app.models.governance import ComplianceIssue, PolicyAcknowledgement
    from app.models.social import EmployeeParticipation, ParticipationStatus
    from app.models.user import User
    from app.models.gamification import Badge, Reward

    for award in db.query(BadgeAward).order_by(BadgeAward.awarded_at.desc()).limit(50).all():
        user = db.query(User).filter(User.id == award.user_id).first()
        badge = db.query(Badge).filter(Badge.id == award.badge_id).first()
        events.append({
            "type": "badge_unlock",
            "timestamp": award.awarded_at,
            "title": f"{user.full_name if user else 'User'} earned '{badge.name if badge else 'Badge'}'",
            "icon": "🏅",
        })

    for redemption in db.query(RewardRedemption).order_by(RewardRedemption.redeemed_at.desc()).limit(50).all():
        user = db.query(User).filter(User.id == redemption.user_id).first()
        reward = db.query(Reward).filter(Reward.id == redemption.reward_id).first()
        events.append({
            "type": "reward_redeemed",
            "timestamp": redemption.redeemed_at,
            "title": f"{user.full_name if user else 'User'} redeemed '{reward.name if reward else 'Reward'}'",
            "icon": "🎁",
        })

    for issue in db.query(ComplianceIssue).order_by(ComplianceIssue.created_at.desc()).limit(50).all():
        events.append({
            "type": "compliance_issue",
            "timestamp": issue.created_at,
            "title": f"Compliance issue raised: {issue.title}",
            "icon": "⚠️",
        })

    for ack in db.query(PolicyAcknowledgement).order_by(PolicyAcknowledgement.acknowledged_at.desc()).limit(50).all():
        user = db.query(User).filter(User.id == ack.user_id).first()
        events.append({
            "type": "policy_ack",
            "timestamp": ack.acknowledged_at,
            "title": f"{user.full_name if user else 'User'} acknowledged a policy",
            "icon": "📋",
        })

    for p in db.query(EmployeeParticipation).filter(
        EmployeeParticipation.status == ParticipationStatus.approved
    ).order_by(EmployeeParticipation.reviewed_at.desc()).limit(50).all():
        user = db.query(User).filter(User.id == p.user_id).first()
        events.append({
            "type": "csr_approval",
            "timestamp": p.reviewed_at or p.submitted_at,
            "title": f"{user.full_name if user else 'User'}'s CSR participation approved",
            "icon": "🌱",
        })

    events.sort(key=lambda e: e["timestamp"] or datetime.min, reverse=True)
    return events[offset: offset + limit]
