# research_sources.py
# SQLAlchemy model for storing research source info

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ResearchSource(Base):
    __tablename__ = "research_sources"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    source_type = Column(String(20), nullable=False)  # ai_suggested/google/arxiv
    url = Column(Text)
    title = Column(Text)
    author = Column(Text, nullable=True)
    publication_date = Column(DateTime, nullable=True)
    source_domain = Column(String(255), nullable=True)
    verification_status = Column(String(20), default="pending")
    relevance_score = Column(DECIMAL(3, 2), nullable=True)
    freshness_score = Column(DECIMAL(3, 2), nullable=True)
    summary = Column(Text, nullable=True)
    key_points = Column(Text, nullable=True)
    is_used = Column(Boolean, default=False)
    verification_attempts = Column(Integer, default=0)
    last_verified_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
