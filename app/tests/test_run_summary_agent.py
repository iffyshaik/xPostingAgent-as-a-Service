"""
Manual test script for the Summary Agent.

This script:
1. Inserts a dummy request and verified sources
2. Runs the summary agent
3. Prints the saved summary and key points
"""

from app.database import SessionLocal
from app.models.requests import Request
from app.models.research_sources import ResearchSource
from app.models.summaries import Summary
from app.agents.summary_agent.core_summary_agent import generate_and_store_summary
import random

def insert_dummy_data():
    """Insert dummy request and sources into DB"""
    with SessionLocal() as session:
        # Step 1: Create request
        request = Request(
            user_id=1,
            original_topic="AI in education",
            content_topic="How AI is transforming personalised learning",
            content_type="article",
            status="summarizing"
        )
        session.add(request)
        session.flush()  # get request.id before commit

        # Step 2: Add 3 dummy verified sources
        summaries = [
            "AI helps tailor lessons to student learning styles and pace.",
            "Data-driven tutoring systems can improve outcomes in underperforming schools.",
            "Challenges include bias in algorithms and data privacy in classrooms."
        ]

        all_key_points = [
            ["AI personalisation improves learning speed"],
            ["AI tutors help struggling students"],
            ["Privacy issues must be addressed"]
        ]

        for i in range(3):
            src = ResearchSource(
                request_id=request.id,
                user_id=1,
                source_type="ai_suggested",
                url=f"https://example.com/{i}",
                title=f"Source {i}",
                author="Test Author",
                verification_status="verified",
                relevance_score=round(random.uniform(0.7, 1.0), 2),
                summary=summaries[i],
                key_points=all_key_points[i],
                is_used=True
            )
            session.add(src)

        session.commit()
        return request.id

def run_test():
    request_id = insert_dummy_data()

    with SessionLocal() as session:
        sources = session.query(ResearchSource).filter_by(request_id=request_id).all()
        source_dicts = [{
            "summary": s.summary,
            "key_points": s.key_points
        } for s in sources]

        request = session.get(Request, request_id)
        generate_and_store_summary(
            request_id=request_id,
            verified_sources=source_dicts,
            target_length=500,
            content_type=request.content_type,
            user_id=request.user_id
        )

        summary = session.query(Summary).filter_by(request_id=request_id).first()
        print("\n--- Summary Agent Output ---")
        print("Summary:\n", summary.combined_summary)
        print("\nKey Points:")
        for point in summary.combined_key_points:
            print("-", point)

if __name__ == "__main__":
    run_test()
