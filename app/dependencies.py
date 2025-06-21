# app/dependencies.py
"""
Shared FastAPI dependency functions.

These are injected into routes or services using Depends(...).
- get_db(): provides a SQLAlchemy session
- get_current_user(): extracts the current user ID from the JWT token

These are used across routes for authentication, database access, etc.
"""

from app.database import SessionLocal

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
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
def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
