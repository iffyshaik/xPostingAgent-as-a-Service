# scripts/insert_test_content.py

"""
Standalone script to insert a test row into content_queue
for platform integration testing.
"""

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.content_queue import ContentQueue
from app.models.requests import Request
from app.models.users import User

# Make sure this script runs from root (not inside app/)
db = SessionLocal()

def insert_test_data():
    # Ensure test user exists
    user = db.query(User).filter_by(email="testuser@example.com").first()
    if not user:
        user = User(
            email="testuser@example.com",
            password_hash="hashed-password",  # no auth needed for now
            subscription_tier="free",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Insert request row (needed FK)
    request = Request(
        user_id=user.id,
        original_topic="How AI transforms education",
        content_topic="How AI tutors are changing the classroom",
        status="ready",
        content_type="thread",
        platform="typefully",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(request)
    db.commit()
    db.refresh(request)

    # Insert content_queue row
    content = ContentQueue(
        request_id=request.id,
        user_id=user.id,
        content_type="thread",
        generated_content="This is a test content for Typefully.\nThread line 1\nThread line 2",
        status="approved",
        scheduled_for=datetime.utcnow() + timedelta(minutes=1),  # schedule in near future
        platform="typefully",
        created_at=datetime.utcnow()
    )
    db.add(content)
    db.commit()
    db.refresh(content)

    print(f"✅ Inserted content ID {content.id} for testing.")
    return content.id

if __name__ == "__main__":
    content_id = insert_test_data()
