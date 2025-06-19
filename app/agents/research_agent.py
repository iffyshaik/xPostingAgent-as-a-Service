# research_agent.py
# Uses AI to suggest sources, verifies them, and stores verified results in the database

from app.llm.engine import generate_completion
from app.prompts.research_prompt import build_research_prompt
from app.database import SessionLocal
from app.models.research_sources import ResearchSource
from sqlalchemy.exc import SQLAlchemyError
import requests
from datetime import datetime

def verify_url(url: str) -> bool:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        )
    }
    try:
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        if response.status_code < 400:
            return True
        # fallback to GET if HEAD is not allowed
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code < 400
    except Exception as e:
        print(f"❌ Exception during URL check: {e}")
        return False


def parse_ai_response(response_text: str):
    sources = []
    lines = response_text.strip().split("\n")
    for line in lines:
        parts = line.split(" - ")
        if len(parts) == 2:
            title_author = parts[0].split(".", 1)[-1].strip('" ').strip()
            url = parts[1].strip().strip("[]")
            sources.append({
                "title_author": title_author,
                "url": url
            })
    return sources

def generate_research_sources(request_id: int, content_topic: str, user_id: int, limit: int = 5, preference: str = "balanced"):
    db = SessionLocal()
    try:
        prompt = build_research_prompt(content_topic, preference)
        print("\n🧠 Prompt sent to LLM:")
        print(prompt)

        ai_response = generate_completion(prompt, agent="research_agent")
        print("\n📥 Raw AI Response:")
        print(ai_response)

        raw_sources = parse_ai_response(ai_response)
        print(f"\n🔍 Parsed {len(raw_sources)} source(s):")
        for src in raw_sources:
            print(f"- {src['title_author']} | {src['url']}")

        verified = 0
        for source in raw_sources:
            url = source["url"]

            # ✅ Skip duplicates for same request
            existing = db.query(ResearchSource).filter_by(request_id=request_id, url=url).first()
            if existing:
                print(f"🔁 Already stored for this request, skipping: {url}")
                continue

            print(f"🔗 Verifying URL: {url}")
            if verify_url(url):
                print("✅ Verified, adding to DB")
                db_source = ResearchSource(
                    request_id=request_id,
                    user_id=user_id,
                    source_type="ai_suggested",
                    url=url,
                    title=source["title_author"],
                    verification_status="verified",
                    relevance_score=0.8,           # 🔧 Placeholder
                    freshness_score=0.7,           # 🔧 Placeholder
                    verification_attempts=1,
                    last_verified_at=datetime.utcnow(),
                )
                db.add(db_source)
                verified += 1

                if verified >= limit:
                    break
            else:
                print("❌ URL failed verification")

        db.commit()

        if verified > 0:
            print(f"\n✅ Success: {verified} verified source(s) stored.")
            return True
        else:
            print(f"\n⚠️ Only {verified} source(s) verified — none stored.")
            return False

    except SQLAlchemyError as e:
        db.rollback()
        print(f"\n🔥 DB Error: {e}")
        return False
    except Exception as e:
        print(f"\n🔥 Unhandled Error: {e}")
        return False
    finally:
        db.close()


