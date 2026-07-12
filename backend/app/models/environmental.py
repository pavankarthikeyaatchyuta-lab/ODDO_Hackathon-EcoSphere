from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class EmissionSourceType(str, enum.Enum):
    purchase = "purchase"
    manufacturing = "manufacturing"
    expense = "expense"
    fleet = "fleet"
    manual = "manual"


class GoalStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    missed = "missed"


class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    source_type = Column(Enum(EmissionSourceType), nullable=False)
    factor_value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    carbon_transactions = relationship("CarbonTransaction", back_populates="emission_factor")


class CarbonTransaction(Base):
    __tablename__ = "carbon_transactions"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    emission_factor_id = Column(Integer, ForeignKey("emission_factors.id"), nullable=True)
    source_type = Column(Enum(EmissionSourceType), nullable=False)
    quantity = Column(Float, nullable=False)
    co2_equivalent = Column(Float, nullable=False)
    description = Column(Text)
    auto_generated = Column(Boolean, default=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    department = relationship("Department", back_populates="carbon_transactions")
    emission_factor = relationship("EmissionFactor", back_populates="carbon_transactions")


class EnvironmentalGoal(Base):
    __tablename__ = "environmental_goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String, nullable=False)
    status = Column(Enum(GoalStatus), default=GoalStatus.active)
    target_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductESGProfile(Base):
    __tablename__ = "product_esg_profiles"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    carbon_footprint = Column(Float, default=0.0)
    recyclability_score = Column(Float, default=0.0)
    sustainability_rating = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
