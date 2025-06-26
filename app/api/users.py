from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user_configurations import UserConfiguration
from app.models.users import User
from app.schemas.user_configurations import UpdateUserConfig


#router = APIRouter()
router = APIRouter(tags=["User Configurations"])

@router.get("/users/configurations")
def get_user_configurations(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    config = (
        db.query(UserConfiguration)
        .filter(UserConfiguration.user_id == current_user_id)
        .first()
    )
    if not config:
        config = UserConfiguration(user_id=current_user_id)
        db.add(config)
        db.commit()
        db.refresh(config)

    return {"success": True, "data": config}


@router.put("/users/configurations")
def update_user_configurations(
    update: UpdateUserConfig,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user),
):
    config = (
        db.query(UserConfiguration)
        .filter(UserConfiguration.user_id == current_user_id)
        .first()
    )

    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    # Update only fields that are set
    for field, value in update.dict(exclude_unset=True).items():
        setattr(config, field, value)

    db.commit()
    db.refresh(config)

    return {"success": True, "data": config}


@router.get("/users/usage-stats")
def get_user_usage_stats(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Return current user's API quota and usage stats.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "success": True,
        "data": {
            "api_quota_daily": user.api_quota_daily,
            "api_quota_used_today": user.api_quota_used_today,
            "quota_reset_date": user.quota_reset_date
        },
        "error": None
    }

