# app/api/dev_patch_summaries.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.research_sources import ResearchSource

router = APIRouter(tags=["Dev Utilities"])

@router.post("/dev/patch-summaries/{request_id}")
def patch_summaries(request_id: int, db: Session = Depends(get_db)):
    sources = db.query(ResearchSource).filter_by(
        request_id=request_id,
        verification_status="verified"
    ).all()

    for s in sources:
        s.summary = "This is a mock summary for testing the summary agent."
        s.key_points = ["Point A", "Point B", "Point C"]

    db.commit()
    return {"success": True, "patched": len(sources)}
