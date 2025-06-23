"""
SQLAlchemy model for storing summarised research content
linked to a user's content generation request.
"""

from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, ARRAY, TIMESTAMP, func
from app.database import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    combined_summary = Column(Text, nullable=False)
    combined_key_points = Column(ARRAY(Text), nullable=False)
    source_count = Column(Integer, nullable=False)
    is_used = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

