from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.environmental import EmissionFactor
from app.schemas.environmental import (
    CarbonTransactionCreate, CarbonTransactionOut,
    EnvironmentalGoalCreate, EnvironmentalGoalUpdate, EnvironmentalGoalOut,
    EmissionFactorCreate, EmissionFactorOut,
)
from app.services import environmental_service

router = APIRouter(prefix="/api/environmental", tags=["environmental"])


@router.get("/emission-factors", response_model=List[EmissionFactorOut])
def list_factors(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(EmissionFactor).all()


@router.post("/emission-factors", response_model=EmissionFactorOut, status_code=201)
def create_factor(data: EmissionFactorCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    factor = EmissionFactor(**data.model_dump())
    db.add(factor)
    db.commit()
    db.refresh(factor)
    return factor


@router.get("/emissions", response_model=List[CarbonTransactionOut])
def list_emissions(department_id: int = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return environmental_service.get_transactions(db, department_id)


@router.post("/emissions", response_model=CarbonTransactionOut, status_code=201)
def create_emission(data: CarbonTransactionCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return environmental_service.create_carbon_transaction(db, data)


@router.get("/goals", response_model=List[EnvironmentalGoalOut])
def list_goals(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return environmental_service.get_goals(db)


@router.post("/goals", response_model=EnvironmentalGoalOut, status_code=201)
def create_goal(data: EnvironmentalGoalCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return environmental_service.create_goal(db, data)


@router.patch("/goals/{goal_id}", response_model=EnvironmentalGoalOut)
def update_goal(goal_id: int, data: EnvironmentalGoalUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return environmental_service.update_goal(db, goal_id, data)
