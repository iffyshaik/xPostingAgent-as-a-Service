# scripts/wipe_all_data.py

"""
Deletes all data from every table in a safe order.
Does NOT delete schema. Keeps tables and relationships intact.
"""

from app.database import SessionLocal
from sqlalchemy import text

def wipe_all_tables():
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
        print("✅ All tables truncated successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error truncating tables: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    wipe_all_tables()
