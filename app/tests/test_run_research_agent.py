"""
Manual Test for Research Agent
------------------------------
Runs the full research pipeline using AI + Google search + filtering + DB insert.
"""

from app.agents.research_agent.core_research_agent import generate_research_sources
from app.models.requests import Request
from app.models.users import User
from app.database import SessionLocal
import datetime

# 🧪 Setup test user + request
db = SessionLocal()

# Use or create test user
user = db.query(User).filter_by(email="test@example.com").first()
if not user:
    user = User(
        email="test@example.com",
        password_hash="fake",
        subscription_tier="free",
        api_quota_daily=5,
        api_quota_used_today=0,
        quota_reset_date=datetime.date.today(),
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(user)
    db.commit()

# Create new request with content_topic
test_topic = "Impact of AI on education systems"
req = Request(
    user_id=user.id,
    original_topic=test_topic,
    content_topic=test_topic,
    status="researching",
    content_type="thread"
)

# Save user_id safely before session closes
user_id = user.id

db.add(req)
db.commit()
db.refresh(req)
db.close()

# Run the agent
print("\n🚀 Running Research Agent...\n")
success = generate_research_sources(
    request_id=req.id,
    content_topic=test_topic,
    user_id=user_id,
    limit=5,
    preference="balanced"
)

print("\n✅ Research Agent Result:", "Success" if success else "No good sources found")
