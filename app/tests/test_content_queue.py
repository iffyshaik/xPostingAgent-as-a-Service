# app/tests/test_content_queue.py
"""
Tests for content queue service functions:
- approve_content()
- schedule_content()
- post_content()

These are unit tests using a mock/test DB session.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.content_queue import ContentQueue
from app.services.content_queue import (
    approve_content,
    schedule_content,
    post_content,
)
from app.database import Base


# ---------- SETUP: In-memory DB for testing ----------
TEST_DATABASE_URL = "sqlite:///:memory:"  # Fast, RAM-only

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    from app.models.content_queue import ContentQueue
    ContentQueue.__table__.create(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        ContentQueue.__table__.drop(bind=engine)


# ---------- FIXTURE: Sample draft content ----------
@pytest.fixture
def draft_content(db):
    content = ContentQueue(
        request_id=1,
        user_id=1,
        content_type="article",
        generated_content="This is a test article with enough words to pass validation.",
        status="draft",
        platform="x"
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


# ---------- TEST: Approve Content ----------
def test_approve_content_success(db, draft_content):
    response = approve_content(content_id=draft_content.id, db=db)
    updated = db.query(ContentQueue).get(draft_content.id)

    assert response["success"] is True
    assert updated.status == "approved"


# ---------- TEST: Schedule Content ----------
def test_schedule_content_success(db, draft_content):
    approve_content(content_id=draft_content.id, db=db)  # must be approved first
    schedule_time = datetime.utcnow() + timedelta(hours=1)

    response = schedule_content(draft_content.id, schedule_time, db)
    updated = db.query(ContentQueue).get(draft_content.id)

    assert response["success"] is True
    assert updated.status == "scheduled"
    assert updated.scheduled_for == schedule_time


# ---------- TEST: Post Content ----------
def test_post_content_success(db, draft_content):
    approve_content(draft_content.id, db)
    draft_content.status = "scheduled"
    db.commit()

    response = post_content(draft_content.id, db)
    updated = db.query(ContentQueue).get(draft_content.id)

    assert response["success"] is True
    assert updated.status == "posted"
    assert updated.posted_at is not None
    assert "post_id" in updated.post_response
