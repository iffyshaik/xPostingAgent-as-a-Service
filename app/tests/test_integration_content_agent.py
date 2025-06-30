# 📁 File: app/tests/test_integration_content_agent.py

"""
Integration Test: Content Agent
Tests that create_content() generates and stores content_queue and thread_metadata correctly.
"""

import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.requests import Request
from app.models.summaries import Summary
from app.models.content_queue import ContentQueue
from app.models.thread_metadata import ThreadMetadata
from app.agents.content_agent.core_content_agent import create_content
from app.database import SessionLocal


@pytest.mark.integration
def test_create_content_end_to_end_with_mocked_llm():
    """End-to-end integration test with mocked LLM for a 'thread' request."""

    db: Session = SessionLocal()

    # --- Insert mock request ---
    request = Request(
        #id=9999,
        user_id=1,
        content_type="thread",
        thread_tweet_count=5,
        include_source_citations=True,
        citation_count=2,
        platform="x",
        original_topic="How AI is changing everything.",
        content_topic="How AI will reshape creativity.",
        status="creating",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(request)
    db.flush()

    # --- Insert mock summary ---
    summary = Summary(
        request_id=request.id,
        user_id=1,
        combined_summary="AI will change everything.",
        combined_key_points=["Data", "Personalisation", "Automation"],
        source_count=5,
        created_at=datetime.utcnow(),
    )
    db.add(summary)
    db.commit()

    # --- User config passed as dict ---
    user_config = {
        "persona": "Tech-savvy founder",
        "tone": "optimistic",
        "style": "conversational",
        "language": "en"
    }

    # --- Patch LLM call ---
    with patch("app.agents.content_agent.generate_completion") as mock_llm:
        mock_llm.return_value = "🧵 Tweet 1\nTweet 2\nTweet 3\nTweet 4\nTweet 5"

        # --- ACT: call content agent ---
        content = create_content(
            db=db,
            request=request,
            summary=summary,
            research_sources=[],
            user_config=user_config
        )

        # --- ASSERT: ContentQueue ---
        assert content is not None
        assert content.status == "draft"
        assert "Tweet 1" in content.generated_content
        assert content.content_type == "thread"

        # --- ASSERT: ThreadMetadata ---
        meta = db.query(ThreadMetadata).filter_by(content_queue_id=content.id).first()
        assert meta is not None
        assert meta.requested_tweet_count == 5
        assert meta.actual_tweet_count == 5
        assert isinstance(meta.thread_structure, list)
        assert len(meta.thread_structure) == 5

        # --- ASSERT: LLM Called as expected ---
        assert mock_llm.called
        prompt_sent = mock_llm.call_args[0][0]
        assert "Tech-savvy founder" in prompt_sent
        assert "AI will change everything" in prompt_sent

    # --- Clean up ---
    db.query(ThreadMetadata).filter_by(content_queue_id=content.id).delete()
    db.query(ContentQueue).filter_by(id=content.id).delete()
    db.query(Summary).filter_by(request_id=9999).delete()
    db.query(Request).filter_by(id=9999).delete()
    db.commit()
    db.close()
