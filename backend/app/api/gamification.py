from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.gamification import (
    ChallengeCreate, ChallengeUpdate, ChallengeOut,
    BadgeCreate, BadgeOut,
    RewardCreate, RewardOut, RedemptionOut,
)
from app.services import gamification_service
from app.services.business_rules_service import redeem_reward

router = APIRouter(prefix="/api/gamification", tags=["gamification"])


@router.get("/challenges", response_model=List[ChallengeOut])
def list_challenges(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    from app.models.gamification import Challenge
    return db.query(Challenge).order_by(Challenge.created_at.desc()).all()


@router.post("/challenges", response_model=ChallengeOut, status_code=201)
def create_challenge(data: ChallengeCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return gamification_service.create_challenge(db, data)


@router.patch("/challenges/{challenge_id}", response_model=ChallengeOut)
def update_challenge(challenge_id: int, data: ChallengeUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return gamification_service.update_challenge(db, challenge_id, data)


@router.post("/challenges/{challenge_id}/join")
def join_challenge(challenge_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return gamification_service.join_challenge(db, challenge_id, current_user.id)


@router.post("/challenges/{challenge_id}/complete")
def complete_challenge(challenge_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return gamification_service.complete_challenge(db, challenge_id, current_user.id)


@router.get("/badges", response_model=List[BadgeOut])
def list_badges(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return gamification_service.get_badges(db)


@router.post("/badges", response_model=BadgeOut, status_code=201)
def create_badge(data: BadgeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return gamification_service.create_badge(db, data)


@router.get("/my-badges")
def my_badges(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return gamification_service.get_user_badges(db, current_user.id)


@router.get("/rewards", response_model=List[RewardOut])
def list_rewards(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return gamification_service.get_rewards(db)


@router.post("/rewards", response_model=RewardOut, status_code=201)
def create_reward(data: RewardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return gamification_service.create_reward(db, data)


@router.post("/rewards/{reward_id}/redeem", response_model=RedemptionOut)
def redeem(reward_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return redeem_reward(db, current_user.id, reward_id)


@router.get("/leaderboard")
def leaderboard(limit: int = 20, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    users = gamification_service.get_leaderboard(db, limit)
    return [{"id": u.id, "full_name": u.full_name, "xp_points": u.xp_points, "department_id": u.department_id} for u in users]
