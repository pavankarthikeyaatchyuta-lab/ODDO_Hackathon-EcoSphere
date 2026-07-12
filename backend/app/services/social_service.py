from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.social import CSRActivity, EmployeeParticipation, ParticipationStatus, Training
from app.models.settings import AppSettings
from app.schemas.social import CSRActivityCreate, ParticipationCreate, ParticipationApprove, TrainingCreate
from app.models.notification import NotificationType
from app.services.notification_service import create_notification
from datetime import datetime


def is_evidence_required(db: Session) -> bool:
    setting = db.query(AppSettings).filter(AppSettings.key == "evidence_requirement").first()
    return setting is not None and setting.value == "true"


def create_csr_activity(db: Session, data: CSRActivityCreate) -> CSRActivity:
    activity = CSRActivity(**data.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_csr_activities(db: Session, department_id: int = None):
    q = db.query(CSRActivity)
    if department_id:
        q = q.filter(CSRActivity.department_id == department_id)
    return q.order_by(CSRActivity.created_at.desc()).all()


def join_activity(db: Session, user_id: int, data: ParticipationCreate) -> EmployeeParticipation:
    existing = db.query(EmployeeParticipation).filter(
        EmployeeParticipation.activity_id == data.activity_id,
        EmployeeParticipation.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already joined this activity")
    p = EmployeeParticipation(activity_id=data.activity_id, user_id=user_id, notes=data.notes)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def upload_evidence(db: Session, participation_id: int, user_id: int, file_path: str):
    p = db.query(EmployeeParticipation).filter(
        EmployeeParticipation.id == participation_id,
        EmployeeParticipation.user_id == user_id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Participation not found")
    p.evidence_file = file_path
    db.commit()
    return p


def approve_participation(db: Session, participation_id: int, data: ParticipationApprove) -> EmployeeParticipation:
    p = db.query(EmployeeParticipation).filter(EmployeeParticipation.id == participation_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Participation not found")

    if data.status == ParticipationStatus.approved and is_evidence_required(db):
        if not p.evidence_file:
            raise HTTPException(status_code=400, detail="Evidence file required before approval")

    p.status = data.status
    p.reviewed_at = datetime.utcnow()
    if data.notes:
        p.notes = data.notes

    if data.status == ParticipationStatus.approved:
        activity = db.query(CSRActivity).filter(CSRActivity.id == p.activity_id).first()
        if activity and activity.xp_reward:
            from app.models.user import User
            user = db.query(User).filter(User.id == p.user_id).first()
            if user:
                user.xp_points += activity.xp_reward
        create_notification(
            db, p.user_id, NotificationType.csr_approval,
            "CSR Participation Approved",
            f"Your participation has been approved. You earned {activity.xp_reward if activity else 0} XP!"
        )

    db.commit()
    db.refresh(p)
    return p


def create_training(db: Session, data: TrainingCreate) -> Training:
    training = Training(**data.model_dump())
    db.add(training)
    db.commit()
    db.refresh(training)
    return training


def get_trainings(db: Session):
    return db.query(Training).order_by(Training.created_at.desc()).all()
