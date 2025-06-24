# app/api/user_config_seed.py
"""
TEMP: Create user_config for current user. Only needed for manual testing.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user_configurations import UserConfiguration

router = APIRouter(tags=["Dev Utilities"])

@router.post("/dev/create-user-config")
def create_user_config(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing = db.query(UserConfiguration).filter_by(user_id=user_id).first()
    if existing:
        return {"message": "User config already exists", "user_id": user_id}

    config = UserConfiguration(
        user_id=user_id,
        persona="Tech-savvy and concise",
        tone="informative",
        style="engaging",
        language="en",
        research_preference="balanced",
        platform_preference="typefully"
    )
    db.add(config)
    db.commit()
    return {"success": True, "user_id": user_id}
