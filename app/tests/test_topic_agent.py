# tests/test_topic_agent.py

"""
Test for Topic Generation Agent
Simulates topic refinement using a mocked LLM.
"""

import pytest
from unittest.mock import patch
from app.agents.topic_agent import generate_content_topic
from app.models.requests import Request
from app.database import SessionLocal, Base, engine
from app.models.users import User

# Set up a temporary in-memory database for isolated testing
@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ✅ Insert dummy user with id=1
    dummy_user = User(id=1, email="test@example.com", password_hash="dummy")
    db.add(dummy_user)
    db.commit()

    # ✅ Then insert request row linked to that user
    dummy_request = Request(
        id=999,
        user_id=1,
        original_topic="How AI is changing education",
        content_type="thread",
        status="pending"
    )
    db.add(dummy_request)
    db.commit()

    yield #Everything after "yield" runs after the test (so guarantee tests are clean, repeatable and safe)

    # ✅ Clean up
    db.query(Request).filter_by(id=999).delete()
    db.query(User).filter_by(id=1).delete()
    db.commit()
    db.close()
    Base.metadata.drop_all(bind=engine)



@patch("app.agents.topic_agent.generate_completion")
def test_generate_content_topic(mock_llm, setup_db):
    """
    Test that generate_content_topic refines a topic and updates the DB.
    """
    mock_llm.return_value = "5 ways AI is transforming classroom learning"

    refined = generate_content_topic(
        request_id=999,
        original_topic="How AI is changing education",
        user_config={"persona": "Insightful teacher", "tone": "curious", "style": "storytelling"},
        content_type="thread",
        user_id=1
    )

    assert refined == "5 ways AI is transforming classroom learning"

    # Verify DB was updated
    db = SessionLocal()
    req = db.query(Request).filter_by(id=999).one()
    assert req.content_topic == refined
    assert req.status == "researching"
    db.close()
