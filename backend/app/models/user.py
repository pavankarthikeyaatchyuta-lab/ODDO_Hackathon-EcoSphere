from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.employee, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    xp_points = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    department = relationship("Department", back_populates="users")
    notifications = relationship("Notification", back_populates="user")
    badge_awards = relationship("BadgeAward", back_populates="user")
    reward_redemptions = relationship("RewardRedemption", back_populates="user")
    challenge_participations = relationship("ChallengeParticipation", back_populates="user")
    policy_acknowledgements = relationship("PolicyAcknowledgement", back_populates="user")
