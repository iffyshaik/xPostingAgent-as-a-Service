# Phase 1: Core Infrastructure - FastAPI & Authentication

## Goal
Build a basic FastAPI app with JWT-based authentication and user session management.

## Prerequisites
- FastAPI
- Pydantic
- Uvicorn
- Passlib (for hashing passwords)
- PyJWT or equivalent

## Step 1: Install Dependencies
```bash
pip install fastapi uvicorn passlib[bcrypt] python-jose
```

## Step 2: FastAPI App Structure
Create `app/main.py`:
```python
from fastapi import FastAPI
from app.api import auth

app = FastAPI()
app.include_router(auth.router, prefix="/auth")
```

Create `app/api/auth.py`:
```python
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(payload: UserRegister):
    return register_user(payload)

@router.post("/login")
def login(payload: UserLogin):
    return login_user(payload)
```

## Step 3: Auth Service Logic
Create `app/services/auth_service.py`:
```python
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Hashing

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)

# JWT Generation

def create_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

## Step 4: Session Management (UserSessions Table)
Track issued tokens in `user_sessions` table with expiry:
- Store `token_hash`, `user_id`, `expires_at`
- Invalidate on logout or expiry check

## Step 5: Authentication Dependency
Create `get_current_user` dependency in `auth_service.py`:
```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
        # Query DB for user existence here
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Completion Criteria
- [x] FastAPI app runs with `/auth/register` and `/auth/login`
- [x] Passwords hashed and stored securely
- [x] JWT tokens issued and verified
- [x] Sessions stored and tracked in DB

## Next Step
Build request handling for the Topic Generation Agent and integrate it with user authentication.

---

> **Ensure auth logic is modular. Future agents will use `get_current_user` to scope data to logged-in users.**
