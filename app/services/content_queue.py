# app/services/content_queue.py
"""
Handles the business logic for content queue management:
- Approval (validation + offensive check)
- Scheduling
- Simulated posting (to be replaced by real Typefully/X integration)
"""

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.content_queue import ContentQueue
from app.services.content_validation import validate_article_length, validate_thread_structure
from app.utils.offensive_filter import check_offensive_content


# --- Approve content after validation ---
def approve_content(content_id: int, db: Session):
    """
    Validates the content and sets status to 'approved' if checks pass.
    Raises HTTPException if validation fails.
    """
    content = db.query(ContentQueue).filter(ContentQueue.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft content can be approved")

    # Step 1: Validate structure
    if content.content_type == "article":
        validate_article_length(content.generated_content, max_words=5000)
    elif content.content_type == "thread":
        import json
        tweets = json.loads(content.generated_content)
        validate_thread_structure(tweets, max_tweets=10, max_chars=280)
    else:
        raise HTTPException(status_code=400, detail="Unknown content type")

    # Step 2: Offensive check (if enabled)
    if check_offensive_content(content.generated_content):
        raise HTTPException(status_code=400, detail="Content flagged as offensive")

    # Step 3: Approve
    content.status = "approved"
    db.commit()

    return {"success": True, "message": "Content approved"}


# --- Schedule content for future posting ---
def schedule_content(content_id: int, scheduled_for: datetime, db: Session):
    """
    Schedules approved content for future posting.
    Validates datetime and sets status = 'scheduled'.
    """
    content = db.query(ContentQueue).filter(ContentQueue.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.status != "approved":
        raise HTTPException(status_code=400, detail="Only approved content can be scheduled")

    if scheduled_for < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")

    # Optional: Validate platform compatibility here
    content.scheduled_for = scheduled_for
    content.status = "scheduled"

    db.commit()
    return {"success": True, "message": "Content scheduled"}


# --- Post content immediately (simulated) ---
def post_content(content_id: int, db: Session):
    """
    Simulates posting the content.
    Sets status to 'posted' or 'failed' depending on result.
    This will later call the real Typefully/X API.
    """
    content = db.query(ContentQueue).filter(ContentQueue.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.status not in ["scheduled", "approved"]:
        raise HTTPException(status_code=400, detail="Only approved or scheduled content can be posted")

    try:
        # Simulate post response (replace with real API call later)
        response = {
            "platform": content.platform,
            "status": "success",
            "post_id": f"mock-{content.id}-{datetime.utcnow().isoformat()}"
        }

        content.status = "posted"
        content.posted_at = datetime.utcnow()
        content.post_response = str(response)

    except Exception as e:
        content.status = "failed"
        content.error_message = str(e)

    db.commit()
    return {"success": True, "message": f"Content marked as {content.status}"}
