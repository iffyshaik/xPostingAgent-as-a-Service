# user_configurations.py
# Stores each user's content generation preferences

import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base

class UserConfiguration(Base):
    __tablename__ = "user_configurations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    persona = Column(Text, default="Professional and engaging")
    tone = Column(String(100), default="informative")
    style = Column(String(100), default="conversational")
    language = Column(String(10), default="en")
    default_source_count = Column(Integer, default=5)
    research_preference = Column(String(50), default="balanced")
    platform_preference = Column(String(20), default="typefully")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
