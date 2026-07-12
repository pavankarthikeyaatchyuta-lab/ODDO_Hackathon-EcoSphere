from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.settings import AppSettings
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentOut

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingUpdate(BaseModel):
    value: str
    description: Optional[str] = None


@router.get("/app")
def get_settings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(AppSettings).all()


@router.put("/app/{key}")
def upsert_setting(
    key: str,
    data: SettingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    if not setting:
        setting = AppSettings(key=key)
        db.add(setting)
    setting.value = data.value
    if data.description:
        setting.description = data.description
    db.commit()
    db.refresh(setting)
    return setting


@router.get("/departments", response_model=List[DepartmentOut])
def list_departments(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Department).all()


@router.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    dept = Department(**data.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept
