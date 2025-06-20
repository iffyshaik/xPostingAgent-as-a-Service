# 📁 File: app/models/content_queue.py
"""
SQLAlchemy model for the content_queue table.
Stores generated content drafts, status, scheduling info, and platform metadata.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ContentQueue(Base):
    __tablename__ = "content_queue"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    content_type = Column(String(20), nullable=False)  # "thread" or "article"
    generated_content = Column(Text, nullable=False)
    status = Column(String(20), default="draft")  # draft/approved/posted/flagged/scheduled
    scheduled_for = Column(DateTime, nullable=True)
    platform = Column(String(20), nullable=False)
    post_response = Column(Text, nullable=True)  # API response from X/Typefully
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    posted_at = Column(DateTime, nullable=True)

    # Optional: relationships
    request = relationship("Request", backref="content_queue")
    user = relationship("User", backref="content_queue")
