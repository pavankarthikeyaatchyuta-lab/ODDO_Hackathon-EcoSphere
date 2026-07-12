from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.gamification import (
    Challenge, ChallengeParticipation, Badge, BadgeAward, Reward, RewardRedemption
)
from app.schemas.gamification import ChallengeCreate, ChallengeUpdate, BadgeCreate, RewardCreate
from app.models.notification import NotificationType
from app.services.notification_service import create_notification


def create_challenge(db: Session, data: ChallengeCreate) -> Challenge:
    challenge = Challenge(**data.model_dump())
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


def update_challenge(db: Session, challenge_id: int, data: ChallengeUpdate) -> Challenge:
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(challenge, k, v)
    db.commit()
    db.refresh(challenge)
    return challenge


def join_challenge(db: Session, challenge_id: int, user_id: int) -> ChallengeParticipation:
    existing = db.query(ChallengeParticipation).filter(
        ChallengeParticipation.challenge_id == challenge_id,
        ChallengeParticipation.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already joined this challenge")
    p = ChallengeParticipation(challenge_id=challenge_id, user_id=user_id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def complete_challenge(db: Session, challenge_id: int, user_id: int) -> ChallengeParticipation:
    p = db.query(ChallengeParticipation).filter(
        ChallengeParticipation.challenge_id == challenge_id,
        ChallengeParticipation.user_id == user_id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Not joined this challenge")
    if p.completed:
        raise HTTPException(status_code=400, detail="Already completed")

    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    p.completed = True
    p.completed_at = datetime.utcnow()

    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if user and challenge:
        user.xp_points += challenge.xp_reward

    db.commit()

    from app.services.business_rules_service import check_and_award_badges
    check_and_award_badges(db, user_id)

    db.refresh(p)
    return p


def get_leaderboard(db: Session, limit: int = 20):
    from app.models.user import User
    return (
        db.query(User)
        .filter(User.is_active == True)
        .order_by(User.xp_points.desc())
        .limit(limit)
        .all()
    )


def create_badge(db: Session, data: BadgeCreate) -> Badge:
    badge = Badge(**data.model_dump())
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


def get_badges(db: Session):
    return db.query(Badge).all()


def get_user_badges(db: Session, user_id: int):
    return db.query(BadgeAward).filter(BadgeAward.user_id == user_id).all()


def create_reward(db: Session, data: RewardCreate) -> Reward:
    reward = Reward(**data.model_dump())
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


def get_rewards(db: Session):
    return db.query(Reward).filter(Reward.is_active == True).all()
