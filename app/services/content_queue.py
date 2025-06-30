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

from app.services.platform_publisher import post_to_typefully, post_to_x
from app.models.thread_metadata import ThreadMetadata
from app.config import settings
from sqlalchemy.exc import SQLAlchemyError
import logging


# --- Approve content after validation ---
def approve_content(content_id: int, db: Session):
    """
    Validates the content and sets status to 'approved' if checks pass.
    Raises HTTPException if validation fails.
    """
    content = db.query(ContentQueue).filter(ContentQueue.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    print("DEBUG: content.status =", content.status)

    if content.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft content can be approved")

    # Step 1: Validate structure
    if content.content_type == "article":
        validate_article_length(content.generated_content, max_words=5000)
    elif content.content_type == "thread":
        import json

        try:
            # Try structured format first (e.g. ["tweet 1", "tweet 2"])
            tweets = json.loads(content.generated_content)
            assert isinstance(tweets, list)
        except (json.JSONDecodeError, AssertionError):
            # Fallback to naive newline splitting
            tweets = [line.strip() for line in content.generated_content.split("\n") if line.strip()]

        validate_thread_structure(tweets, max_tweets=10, max_chars=280)
    else:
        raise HTTPException(status_code=400, detail="Unknown content type")

    # Step 2: Offensive check (if enabled)
    # if check_offensive_content(content.generated_content):
    #     raise HTTPException(status_code=400, detail="Content flagged as offensive")

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

    if content.status in ["posted", "scheduled_deleted", "failed"]:
        raise HTTPException(status_code=400, detail=f"Content in status '{content.status}' cannot be scheduled")
    
    from datetime import timezone
    # Ensure scheduled_for is timezone-aware
    if scheduled_for.tzinfo is None:
        scheduled_for = scheduled_for.replace(tzinfo=timezone.utc)

    if scheduled_for < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future")
    # if scheduled_for < datetime.now(timezone.utc):
    #     raise HTTPException(status_code=400, detail="Scheduled time must be in the future")

    # Optional: Validate platform compatibility here
    content.scheduled_for = scheduled_for
    content.status = "scheduled"
    content.deleted_at = None  # clear deletion if re-scheduling

    db.commit()
    return {"success": True, "message": "Content scheduled"}


# --- Post content immediately (simulated) ---
def post_content(content_id: int, db: Session, dry_run: bool = False) -> dict:
    """
    Posts approved content to the selected platform (Typefully or X).
    If dry_run is True, skip real posting and log simulated result.
    """
    content = db.query(ContentQueue).filter(ContentQueue.id == content_id).first()

    if not content:
        raise ValueError(f"Content with ID {content_id} not found")

    if content.status not in ["approved", "scheduled"]:
        raise ValueError("Content must be approved or scheduled before posting")

    try:
        response = {}
        if dry_run:
            logging.info(f"[DRY RUN] Would post content ID {content.id} to {content.platform}")
            response = {
                "platform_posted_id": "dry_run_id",
                "post_response": "Dry run mode enabled. No request made."
            }

        elif content.platform == "typefully":
            response = post_to_typefully(content.generated_content, scheduled_for=content.scheduled_for)

        elif content.platform == "x":
            # 🔧 TODO: Lookup user's access_token (requires user onboarding flow)
            raise NotImplementedError("Twitter posting not yet implemented. OAuth flow required.")

        else:
            raise ValueError(f"Unsupported platform: {content.platform}")

        # Store result
        content.status = "posted"
        content.posted_at = datetime.utcnow()
        content.post_response = response.get("post_response")
        content.platform_posted_id = response.get("platform_posted_id")
        db.commit()

        return {"success": True, "message": "Posted successfully", "platform_posted_id": content.platform_posted_id}

    except Exception as e:
        logging.error(f"Error posting content ID {content_id}: {e}")
        content.status = "failed"
        content.error_message = str(e)
        db.commit()
        return {"success": False, "message": "Posting failed", "error": str(e)}
    
    

def delete_scheduled_content(content_id: int, db: Session):
    """
    Soft-deletes scheduled content while preserving its audit trail.
    """
    content = db.query(ContentQueue).filter(ContentQueue.id == content_id).first()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.status != "scheduled":
        raise HTTPException(status_code=400, detail="Only scheduled content can be deleted")

    content.deleted_at = datetime.utcnow()
    content.status = "scheduled_deleted"
    content.was_scheduled_then_deleted = True

    db.commit()

    return {"success": True, "message": "Scheduled content deleted"}

