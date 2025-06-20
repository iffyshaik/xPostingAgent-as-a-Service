# 📁 File: app/models/thread_metadata.py
"""
SQLAlchemy model for thread_metadata.
Stores thread structure, requested and actual tweet counts, and citation tweet content.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ThreadMetadata(Base):
    __tablename__ = "thread_metadata"

    id = Column(Integer, primary_key=True, index=True)
    content_queue_id = Column(Integer, ForeignKey("content_queue.id", ondelete="CASCADE"), nullable=False)

    requested_tweet_count = Column(Integer, nullable=False)
    actual_tweet_count = Column(Integer, nullable=False)
    max_tweet_length = Column(Integer, default=280)  # Note: We'll support override from request model soon

    thread_structure = Column(JSON, nullable=False)  # list of tweets as JSON objects
    citation_tweets = Column(JSON, nullable=True)    # optional citation tweet objects

    created_at = Column(DateTime, server_default=func.now())

    # Optional: relationship
    content_queue = relationship("ContentQueue", backref="thread_metadata")
