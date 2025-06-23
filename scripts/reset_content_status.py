# scripts/reset_content_status.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.content_queue import ContentQueue
from datetime import datetime, timedelta

CONTENT_ID = 1  # 🔁 Replace with your ID

if __name__ == "__main__":
    db = SessionLocal()
    content = db.query(ContentQueue).filter_by(id=CONTENT_ID).first()

    if not content:
        print("❌ Content not found.")
    else:
        content.scheduled_for = datetime.utcnow() + timedelta(minutes=2)
        content.status = "approved"
        content.posted_at = None
        content.post_response = None
        content.platform_posted_id = None
        content.error_message = None
        db.commit()
        print(f"✅ Reset content ID {CONTENT_ID} to 'approved'")
