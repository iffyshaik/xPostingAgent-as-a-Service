# users.py
# SQLAlchemy model for platform users

import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    subscription_tier = Column(String(50), default="free")
    api_quota_daily = Column(Integer, default=5)
    api_quota_used_today = Column(Integer, default=0)
    quota_reset_date = Column(Date, default=datetime.date.today)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
