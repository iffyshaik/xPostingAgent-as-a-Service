# insert_dummy_data.py
from app.database import SessionLocal
from app.models.requests import Request
from app.models.users import User
from datetime import datetime

db = SessionLocal()

try:
    # Step 1: Add dummy user
    user = db.query(User).filter_by(id=1).first()
    if not user:
        user = User(
            id=1,
            email="test@example.com",
            password_hash="fakehash"
        )
        db.add(user)
        db.commit()  # ✅ Commit so the user is inserted before using in a foreign key
        print("✅ Dummy user created.")

    # Step 2: Add dummy request
    request = db.query(Request).filter_by(id=101).first()
    if not request:
        request = Request(
            id=101,
            user_id=1,
            original_topic="How AI is changing remote work",
            content_topic="The impact of AI on remote work culture",
            content_type="thread",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(request)
        db.commit()
        print("✅ Dummy request created.")

finally:
    db.close()
    print("✅ Done.")
