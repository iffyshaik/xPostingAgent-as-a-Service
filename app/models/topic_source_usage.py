from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from app.database import Base

class TopicSourceUsage(Base):
    __tablename__ = "topic_source_usage"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content_topic_hash = Column(String(64), nullable=False)
    source_url_hash = Column(String(64), nullable=False)
    usage_count = Column(Integer, default=1)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "content_topic_hash", "source_url_hash", name="uq_user_topic_source"),
    )
