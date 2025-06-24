# app/utils/tokens.py

from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

def create_token(user_id: int) -> str:
    """
    Creates a JWT token for the given user ID.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")
