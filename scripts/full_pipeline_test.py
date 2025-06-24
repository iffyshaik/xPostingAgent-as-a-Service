"""
End-to-end test script for:
User Registration → Topic → Research → Summary → Content → Approve → Schedule → Post (Typefully)
"""

import datetime
import time
from app.database import SessionLocal
from app.models import users, user_configurations, requests
from app.agents.topic_agent import generate_content_topic
from app.agents.research_agent import generate_research_sources
from app.agents.content_agent import create_content
from app.services.content_queue import approve_content, schedule_content, post_content
from app.utils.hash import hash_string

from app.models.requests import Request
from app.models.research_sources import ResearchSource
from app.models.summaries import Summary
from app.models.user_configurations import UserConfiguration


from sqlalchemy import text
from app.agents.summary_agent import generate_and_store_summary




# -----------------------------------------------------------
# STEP 1: Clear DB
# -----------------------------------------------------------
from sqlalchemy import text

def wipe_all_data():
    db = SessionLocal()
    try:
        db.execute(text("""
            TRUNCATE 
                user_sessions,
                thread_metadata,
                content_queue,
                summaries,
                research_sources,
                topic_source_usage,
                requests,
                user_configurations,
                users
            RESTART IDENTITY CASCADE;
        """))
        db.commit()
        print("✅ Database wiped clean.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during wipe_all_data(): {e}")
    finally:
        db.close()


# -----------------------------------------------------------
# STEP 2: Register user + config
# -----------------------------------------------------------
def create_test_user():
    db = SessionLocal()
    existing = db.query(users.User).filter_by(email="test@example.com").first()
    if existing:
        print("⚠️ Test user already exists. Using existing user.")
        user_id = existing.id
        db.close()
        return user_id

    new_user = users.User(
        email="test@example.com",
        password_hash="hashedpassword123",
        subscription_tier="pro",
        api_quota_daily=10,
        api_quota_used_today=0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    config = user_configurations.UserConfiguration(
        user_id=new_user.id,
        persona="Witty and insightful tech founder",
        tone="casual",
        style="threaded storytelling",
        language="en",
        research_preference="balanced",
        platform_preference="typefully"
    )
    db.add(config)
    db.commit()

    user_id = new_user.id
    db.close()
    print("✅ Test user and config created.")
    return user_id


# -----------------------------------------------------------
# STEP 3: Submit a Topic
# -----------------------------------------------------------
def submit_topic(user_id, topic_text="AI and the future of productivity"):
    db = SessionLocal()
    new_request = requests.Request(
        user_id=user_id,
        original_topic=topic_text,
        content_type="thread",
        auto_post=False,
        thread_tweet_count=5,
        include_source_citations=True,
        citation_count=2,
        platform="typefully"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    db.close()
    print(f"✅ Submitted topic: {topic_text}")
    return new_request.id

# -----------------------------------------------------------
# STEP 4: Run Agents (Topic → Research → Summary → Content)
# -----------------------------------------------------------
def run_agents(request_id: int, user_id: int):
    db = SessionLocal()
    request = db.query(Request).filter_by(id=request_id).first()
    config = db.query(UserConfiguration).filter_by(user_id=user_id).first()

    if not request or not config:
        db.close()
        raise ValueError("❌ Missing request or user config")

    config_dict = {
        "persona": config.persona,
        "tone": config.tone,
        "style": config.style,
        "language": config.language,
    }

    print("🧠 Running Topic Agent...")
    content_topic = generate_content_topic(
        request_id,
        request.original_topic,
        config_dict,
        request.content_type,
        user_id
    )

    print("🔎 Running Research Agent...")
    generate_research_sources(
        request_id,
        content_topic,
        user_id,
        limit=config.default_source_count,
        preference=config.research_preference
    )

    print("📝 Running Summary Agent...")
    verified = db.query(ResearchSource)\
        .filter_by(request_id=request_id, verification_status="verified")\
        .filter(ResearchSource.summary.isnot(None))\
        .all()

    verified_sources = []
    for v in verified:
        verified_sources.append({
            "summary": v.summary,
            "key_points": v.key_points.split("\n") if v.key_points else []
        })

    generate_and_store_summary(
        request_id=request_id,
        verified_sources=verified_sources,
        target_length=500,
        content_type=request.content_type,
        user_id=user_id
    )

    print("✍️ Running Content Agent...")
    summary = db.query(Summary).filter_by(request_id=request_id).first()
    create_content(db, request, summary, verified, config_dict)

    db.close()


# -----------------------------------------------------------
# STEP 5: Approve → Schedule → Post
# -----------------------------------------------------------
def approve_schedule_post(request_id):
    db = SessionLocal()
    # Find content queue row
    content_row = db.execute(
        text("SELECT id FROM content_queue WHERE request_id = :rid"),
        {"rid": request_id}
    ).fetchone()

    content_id = content_row[0]
    approve_content(content_id, db)
    print("✅ Content approved.")

    import datetime
    from datetime import timezone

    scheduled_time = datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=15)
    schedule_content(content_id, scheduled_time, db)
    print(f"⏰ Scheduled post for: {scheduled_time}")

    print("⏳ Waiting 5 seconds before posting...")
    time.sleep(5)

    post_result = post_content(content_id, db)
    db.close()
    print("🚀 Posted to Typefully!")
    print("📬 Typefully Response:", post_result)

# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------
if __name__ == "__main__":
    wipe_all_data()
    uid = create_test_user()
    req_id = submit_topic(uid)
    run_agents(req_id, uid)
    approve_schedule_post(req_id)
