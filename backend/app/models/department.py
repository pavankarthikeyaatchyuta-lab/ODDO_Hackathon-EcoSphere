from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="department")
    department_scores = relationship("DepartmentScore", back_populates="department")
    carbon_transactions = relationship("CarbonTransaction", back_populates="department")
    csr_activities = relationship("CSRActivity", back_populates="department")
    audits = relationship("Audit", back_populates="department")
