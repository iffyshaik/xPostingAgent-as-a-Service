# app/dependencies.py
"""
Shared FastAPI dependency functions.

These are injected into routes or services using Depends(...).
- get_db(): provides a SQLAlchemy session
- get_current_user(): extracts the current user ID from the JWT token

These are used across routes for authentication, database access, etc.
"""

from app.database import SessionLocal
from fastapi import Header, HTTPException, status

from jose import jwt, JWTError
from app.config import settings

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

# Dependency: provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency: JWT decoding + user validation
def get_current_user(authorization: str = Header(...)) -> int:
    """
    Extracts and validates user ID from the Bearer token in Authorization header.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")

    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
