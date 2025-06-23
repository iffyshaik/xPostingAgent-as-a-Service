# scripts/run_post_content.py

"""
Standalone script to test posting logic via dry-run.
Uses post_content() from content_queue service.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Ensure local app/ is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Root

from app.database import SessionLocal
from app.services.content_queue import post_content

# Replace this with the ID printed from the insert script
CONTENT_ID = 1  # 🔁 Change this if needed

if __name__ == "__main__":
    db = SessionLocal()
    result = post_content(content_id=CONTENT_ID, db=db, dry_run=False)
    print("✅ Post Content Result:")
    print(result)
