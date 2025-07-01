"""
Source Reuse Tracking
---------------------
Tracks how often a source (URL) is used for a given content topic,
to avoid repetition and promote freshness.
"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from app.database import SessionLocal
from app.models.topic_source_usage import TopicSourceUsage
from app.utils.hash import hash_string
from datetime import datetime

# Default threshold — can pull from DB later if needed
SOURCE_REUSE_THRESHOLD = 3

def is_source_overused(user_id: int, content_topic: str, source_url: str) -> bool:
    """
    Returns True if the source has been used too often for this topic.

    Args:
        content_topic (str): Refined topic
        source_url (str): The source's URL

    Returns:
        bool: True if overused, else False
    """
    topic_hash = hash_string(content_topic)
    url_hash = hash_string(source_url)
    db = SessionLocal()
    try:
        entry = db.query(TopicSourceUsage).filter_by(
            user_id=user_id,
            content_topic_hash=topic_hash,
            source_url_hash=url_hash
        ).first()
        return entry is not None and entry.usage_count >= SOURCE_REUSE_THRESHOLD
    except SQLAlchemyError as e:
        print(f"❌ DB error checking reuse: {e}")
        return False
    finally:
        db.close()


def increment_source_usage(user_id: int, content_topic: str, source_url: str):
    topic_hash = hash_string(content_topic)
    url_hash = hash_string(source_url)
    db = SessionLocal()
    try:
        entry = db.query(TopicSourceUsage).filter_by(
            user_id=user_id,
            content_topic_hash=topic_hash,
            source_url_hash=url_hash
        ).first()

        if entry:
            entry.usage_count += 1
            entry.last_used_at = datetime.utcnow()
        else:
            entry = TopicSourceUsage(
                user_id=user_id,
                content_topic_hash=topic_hash,
                source_url_hash=url_hash,
                usage_count=1,
                last_used_at=datetime.utcnow()
            )
            db.add(entry)

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ DB error saving reuse: {e}")
    finally:
        db.close()
