# requests.py
# Tracks all user-initiated content requests

import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from app.database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original_topic = Column(Text, nullable=False)
    content_topic = Column(Text)
    status = Column(String(50), default="pending")
    content_type = Column(String(20), nullable=False)
    auto_post = Column(Boolean, default=False)
    source_count_limit = Column(Integer, default=5)
    thread_tweet_count = Column(Integer)
    max_article_length = Column(Integer)
    include_source_citations = Column(Boolean, default=False)
    citation_count = Column(Integer, default=1)
    platform = Column(String(20), default="typefully")
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    max_tweet_length = Column(Integer, default=280)
