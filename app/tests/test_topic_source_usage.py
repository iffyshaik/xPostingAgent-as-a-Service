"""
Manual Test for Topic Source Usage Tracking
-------------------------------------------
Run this to verify that incrementing + overuse detection work as expected.
"""

from app.agents.research_agent.services.source_reuse import is_source_overused, increment_source_usage
from app.utils.hash import hash_string
from app.database import SessionLocal
from app.models.topic_source_usage import TopicSourceUsage

from app.models.users import User  # if not already imported

# Insert a test user (only if they don't exist)
db = SessionLocal()
test_user = db.query(User).filter_by(id=9999).first()
if not test_user:
    user = User(id=9999, email="testingdb@example.com", password_hash="fake")
    db.add(user)
    db.commit()
db.close()

# Test inputs
user_id = 9999  # Use a test user ID (won't conflict if not in users table)
topic = "How AI is transforming medicine"
url = "https://example.com/ai-medicine"

# Reset: delete existing entry if it exists
db = SessionLocal()
topic_hash = hash_string(topic)
url_hash = hash_string(url)
db.query(TopicSourceUsage).filter_by(
    user_id=user_id,
    content_topic_hash=topic_hash,
    source_url_hash=url_hash
).delete()
db.commit()
db.close()

# Increment 3 times
for i in range(3):
    print(f"🔁 Incrementing source usage ({i+1}/3)...")
    increment_source_usage(user_id, topic, url)

# Now check if it's overused
is_overused = is_source_overused(user_id, topic, url)
print(f"\n🔍 Is source overused (threshold=3)? {'✅ Yes' if is_overused else '❌ No'}")

# Inspect final DB record
db = SessionLocal()
entry = db.query(TopicSourceUsage).filter_by(
    user_id=user_id,
    content_topic_hash=topic_hash,
    source_url_hash=url_hash
).first()
if entry:
    print(f"\n📊 Final usage count: {entry.usage_count}")
else:
    print("⚠️ No usage entry found")
db.close()
