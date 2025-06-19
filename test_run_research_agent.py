# test_run_research_agent.py
# TEMPORARY TEST SCRIPT
# Run this manually to test that the ResearchAgent fetches and stores verified sources

from app.agents.research_agent import generate_research_sources
from app.database import SessionLocal
from app.models.research_sources import ResearchSource
from sqlalchemy.orm import joinedload

# Parameters for the test
dummy_request_id = 101
dummy_user_id = 1
dummy_topic = "The impact of AI on remote work culture"
preference = "balanced"
source_count = 5

# Run the agent
print("🔍 Running research agent...")
success = generate_research_sources(
    request_id=dummy_request_id,
    content_topic=dummy_topic,
    user_id=dummy_user_id,
    limit=source_count,
    preference=preference
)

# Output results
if success:
    print("✅ Research agent added at least 3 verified sources.")
else:
    print("❌ Research agent failed or did not find enough sources.")

# Display stored sources for visual check
print("\n📦 Retrieved sources from DB:")
db = SessionLocal()
sources = (
    db.query(ResearchSource)
    .filter(ResearchSource.request_id == dummy_request_id)
    .order_by(ResearchSource.id)
    .all()
)

if not sources:
    print("⚠️ No sources found in database.")
else:
    for i, src in enumerate(sources, start=1):
        print(f"{i}. {src.title or 'Untitled'} — {src.url} ({src.verification_status})")

db.close()
