from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil, os, uuid
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.social import (
    CSRActivityCreate, CSRActivityOut,
    ParticipationCreate, ParticipationApprove, ParticipationOut,
    TrainingCreate, TrainingOut, CategoryCreate, CategoryOut,
)
from app.services import social_service
from app.models.social import Category

router = APIRouter(prefix="/api/social", tags=["social"])

UPLOAD_DIR = "/tmp/evidence"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Category).all()


@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    cat = Category(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get("/csr", response_model=List[CSRActivityOut])
def list_csr(department_id: int = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return social_service.get_csr_activities(db, department_id)


@router.post("/csr", response_model=CSRActivityOut, status_code=201)
def create_csr(data: CSRActivityCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return social_service.create_csr_activity(db, data)


@router.post("/csr/join", response_model=ParticipationOut)
def join_csr(data: ParticipationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return social_service.join_activity(db, current_user.id, data)


@router.post("/participations/{participation_id}/evidence")
def upload_evidence(
    participation_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return social_service.upload_evidence(db, participation_id, current_user.id, path)


@router.patch("/participations/{participation_id}/approve", response_model=ParticipationOut)
def approve(
    participation_id: int,
    data: ParticipationApprove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "manager"):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Managers and admins only")
    return social_service.approve_participation(db, participation_id, data)


@router.get("/trainings", response_model=List[TrainingOut])
def list_trainings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return social_service.get_trainings(db)


@router.post("/trainings", response_model=TrainingOut, status_code=201)
def create_training(data: TrainingCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return social_service.create_training(db, data)
