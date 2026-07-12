from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from app.models.gamification import Reward, RewardRedemption, Badge, BadgeAward, ChallengeParticipation
from app.models.governance import ComplianceIssue, ComplianceStatus
from app.models.user import User
from app.models.notification import NotificationType
from app.services.notification_service import create_notification


def redeem_reward(db: Session, user_id: int, reward_id: int) -> RewardRedemption:
    reward = db.query(Reward).filter(Reward.id == reward_id, Reward.is_active == True).first()
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    if reward.stock <= 0:
        raise HTTPException(status_code=400, detail="Reward out of stock")

    user = db.query(User).filter(User.id == user_id).first()
    if user.xp_points < reward.xp_cost:
        raise HTTPException(status_code=400, detail=f"Insufficient XP. Need {reward.xp_cost}, have {user.xp_points}")

    user.xp_points -= reward.xp_cost
    reward.stock -= 1

    redemption = RewardRedemption(reward_id=reward_id, user_id=user_id, xp_spent=reward.xp_cost)
    db.add(redemption)
    db.flush()

    create_notification(
        db, user_id,
        NotificationType.reward_redeemed,
        "Reward Redeemed",
        f"You successfully redeemed '{reward.name}' for {reward.xp_cost} XP"
    )
    db.commit()
    return redemption


def check_and_award_badges(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return

    completed_challenges = (
        db.query(ChallengeParticipation)
        .filter(ChallengeParticipation.user_id == user_id, ChallengeParticipation.completed == True)
        .count()
    )

    existing_badge_ids = {
        a.badge_id for a in db.query(BadgeAward).filter(BadgeAward.user_id == user_id).all()
    }

    badges = db.query(Badge).all()
    newly_awarded = []
    for badge in badges:
        if badge.id in existing_badge_ids:
            continue
        earned = False
        if badge.unlock_rule_type == "xp" and user.xp_points >= badge.unlock_rule_value:
            earned = True
        elif badge.unlock_rule_type == "challenges" and completed_challenges >= badge.unlock_rule_value:
            earned = True

        if earned:
            award = BadgeAward(badge_id=badge.id, user_id=user_id)
            db.add(award)
            db.flush()
            create_notification(
                db, user_id,
                NotificationType.badge_unlock,
                "Badge Unlocked!",
                f"You earned the '{badge.name}' badge!"
            )
            newly_awarded.append(badge)

    db.commit()
    return newly_awarded


def flag_overdue_compliance(db: Session):
    now = datetime.utcnow()
    overdue = (
        db.query(ComplianceIssue)
        .filter(
            ComplianceIssue.due_date < now,
            ComplianceIssue.status.in_([ComplianceStatus.open, ComplianceStatus.in_progress])
        )
        .all()
    )
    for issue in overdue:
        issue.status = ComplianceStatus.overdue
        create_notification(
            db, issue.owner_id,
            NotificationType.overdue_compliance,
            "Compliance Issue Overdue",
            f"Issue '{issue.title}' is past its due date and has been flagged as overdue."
        )
    db.commit()
    return len(overdue)
