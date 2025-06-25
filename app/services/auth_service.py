# app/services/auth_service.py
"""
Business logic for authentication:
- Hashing and verifying passwords
- Creating and decoding JWT tokens
- Fetching the current user from token
"""

from passlib.hash import bcrypt
from jose import jwt, JWTError
from fastapi import HTTPException #Depends all Depends we move to router. keep services clean
from app.config import settings

from sqlalchemy.orm import Session
#from app.database import SessionLocal
#from app.dependencies import get_db 
from app.models.user_sessions import UserSession
import hashlib
#from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone
from app.models.users import User
from app.utils.security import verify_password, hash_password  # assumed location
from app.utils.tokens import create_token       # assumed location

# Dependency to get DB session - Deleted and moved to dependencies.py


# Constants from config
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

# OAuth2 scheme
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password hashing - moved to utils/security
# def hash_password(password: str) -> str:
#     return bcrypt.hash(password)

# def verify_password(password: str, hashed: str) -> bool:
#     return bcrypt.verify(password, hashed)

# JWT generation
def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



# Dummy logic to plug into DB later
# def register_user(payload):
#     # This is a placeholder — you will add DB logic later
#     hashed_pw = hash_password(payload.password)
#     return {"email": payload.email, "hashed_password": hashed_pw}

def register_user(payload, db: Session):
    """
    Registers a new user by hashing the password and storing user info in DB.
    """
    # Check if user already exists
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(payload.password)

    user = User(
        email=payload.email,
        password_hash=hashed_pw
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"success": True, "user_id": user.id, "email": user.email}

def login_user(payload, db: Session):
    """
    Verifies credentials and logs the user in by creating a session and returning a JWT.
    """
    print(f"Login attempt: {payload.email} / {payload.password}")
    user = db.query(User).filter(User.email == payload.email).first()
    
    if not user:
        print("User not found")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user.password_hash):
        print("Password mismatch")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    print("Login successful")
    



    # if not user or not verify_password(payload.password, user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = create_token(user_id=user.id)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expiry = datetime.now(timezone.utc) + timedelta(days=1)

    # Store session
    session = UserSession(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expiry
    )
    db.add(session)
    db.commit()

    # return {
    #     "access_token": token,
    #     "token_type": "bearer",
    #     "user_id": user.id,
    #     "email": user.email
    # }

    return {
        "success": True,
        "data": {
            "token": token,
            "user_id": user.id,
            "email": user.email
        },
        "error": None
    }

