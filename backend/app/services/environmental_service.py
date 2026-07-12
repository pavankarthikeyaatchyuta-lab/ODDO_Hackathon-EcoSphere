from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.environmental import CarbonTransaction, EmissionFactor, EnvironmentalGoal, EmissionSourceType
from app.models.settings import AppSettings
from app.schemas.environmental import CarbonTransactionCreate, EnvironmentalGoalCreate, EnvironmentalGoalUpdate


def is_auto_emission_enabled(db: Session) -> bool:
    setting = db.query(AppSettings).filter(AppSettings.key == "auto_emission_calculation").first()
    return setting is not None and setting.value == "true"


def create_carbon_transaction(db: Session, data: CarbonTransactionCreate) -> CarbonTransaction:
    co2 = data.quantity
    factor = None
    if data.emission_factor_id:
        factor = db.query(EmissionFactor).filter(EmissionFactor.id == data.emission_factor_id).first()
        if factor:
            co2 = round(data.quantity * factor.factor_value, 4)

    tx = CarbonTransaction(
        department_id=data.department_id,
        emission_factor_id=data.emission_factor_id,
        source_type=data.source_type,
        quantity=data.quantity,
        co2_equivalent=co2,
        description=data.description,
        auto_generated=False,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def auto_create_carbon_transaction(
    db: Session, department_id: int, source_type: EmissionSourceType,
    quantity: float, description: str = None
) -> CarbonTransaction:
    factor = db.query(EmissionFactor).filter(EmissionFactor.source_type == source_type).first()
    co2 = round(quantity * factor.factor_value, 4) if factor else quantity

    tx = CarbonTransaction(
        department_id=department_id,
        emission_factor_id=factor.id if factor else None,
        source_type=source_type,
        quantity=quantity,
        co2_equivalent=co2,
        description=description or f"Auto-generated from {source_type.value}",
        auto_generated=True,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_transactions(db: Session, department_id: int = None):
    q = db.query(CarbonTransaction)
    if department_id:
        q = q.filter(CarbonTransaction.department_id == department_id)
    return q.order_by(CarbonTransaction.date.desc()).all()


def create_goal(db: Session, data: EnvironmentalGoalCreate) -> EnvironmentalGoal:
    goal = EnvironmentalGoal(**data.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


def update_goal(db: Session, goal_id: int, data: EnvironmentalGoalUpdate) -> EnvironmentalGoal:
    goal = db.query(EnvironmentalGoal).filter(EnvironmentalGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(goal, k, v)
    db.commit()
    db.refresh(goal)
    return goal


def get_goals(db: Session):
    return db.query(EnvironmentalGoal).order_by(EnvironmentalGoal.created_at.desc()).all()
