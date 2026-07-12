from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType


def create_notification(db: Session, user_id: int, type: NotificationType, title: str, message: str):
    notif = Notification(user_id=user_id, type=type, title=title, message=message)
    db.add(notif)
    db.commit()
    return notif


def get_user_notifications(db: Session, user_id: int, unread_only: bool = False):
    q = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        q = q.filter(Notification.is_read == False)
    return q.order_by(Notification.created_at.desc()).all()


def mark_read(db: Session, notification_id: int, user_id: int):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    if notif:
        notif.is_read = True
        db.commit()
    return notif
