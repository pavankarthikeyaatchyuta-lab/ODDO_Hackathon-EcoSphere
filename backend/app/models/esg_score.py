from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class DepartmentScore(Base):
    __tablename__ = "department_scores"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    environmental_score = Column(Float, default=0.0)
    social_score = Column(Float, default=0.0)
    governance_score = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    period = Column(String, nullable=False)  # e.g. "2024-Q1"
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    department = relationship("Department", back_populates="department_scores")
