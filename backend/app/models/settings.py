from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class ESGWeightSettings(Base):
    __tablename__ = "esg_weight_settings"

    id = Column(Integer, primary_key=True, index=True)
    environmental_weight = Column(Float, default=40.0)
    social_weight = Column(Float, default=30.0)
    governance_weight = Column(Float, default=30.0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class AppSettings(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
    description = Column(String)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
