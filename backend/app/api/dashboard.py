from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.esg_score_service import get_org_esg_score, update_weights
from app.services.activity_feed_service import get_activity_feed
from app.services.notification_service import get_user_notifications, mark_read
from app.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/esg-score")
def esg_score(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_org_esg_score(db)


@router.post("/esg-weights")
def set_weights(
    environmental: float,
    social: float,
    governance: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin only")
    return update_weights(db, environmental, social, governance)


@router.get("/activity")
def activity_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return get_activity_feed(db, limit=limit, offset=offset)


@router.get("/notifications")
def notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_notifications(db, current_user.id, unread_only=unread_only)


@router.patch("/notifications/{notification_id}/read")
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mark_read(db, notification_id, current_user.id)
