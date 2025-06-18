# app/services/auth_service.py
"""
Business logic for authentication:
- Hashing and verifying passwords
- Creating and decoding JWT tokens
- Fetching the current user from token
"""

from passlib.hash import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from app.models.user_sessions import UserSession
import hashlib


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Constants from config
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password hashing
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)

# JWT generation
def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# JWT decoding + user validation
def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dummy logic to plug into DB later
def register_user(payload):
    # This is a placeholder — you will add DB logic later
    hashed_pw = hash_password(payload.password)
    return {"email": payload.email, "hashed_password": hashed_pw}

def login_user(payload, db: Session = Depends(get_db)):
    # In production, verify user from DB
    fake_user_id = 1  # placeholder for actual user ID lookup

    # Generate token
    token = create_token(user_id=fake_user_id)

    # Hash the token for secure storage
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    # Create DB session record
    expiry = datetime.utcnow() + timedelta(days=1)
    session = UserSession(
        user_id=fake_user_id,
        token_hash=token_hash,
        expires_at=expiry
    )
    db.add(session)
    db.commit()

    return {"access_token": token, "token_type": "bearer"}
