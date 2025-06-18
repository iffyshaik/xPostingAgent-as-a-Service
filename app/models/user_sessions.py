# app/models/user_sessions.py
"""
SQLAlchemy model for tracking issued JWT tokens per user.
Used for token expiry, refresh, and logout support.
"""

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.database import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
