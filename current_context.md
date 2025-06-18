# Project Context Handoff

## What We're Building
A multi-tenant SaaS platform that uses AI to generate social media threads and articles from user-submitted topics. It performs research, summarisation, and content creation, and can publish to X (Twitter) or Typefully.

---

## Current Phase
**Phase 1: Core Infrastructure Setup** 🔄 IN PROGRESS

---

## Tech Stack
- Python 3.11+ / FastAPI
- PostgreSQL + SQLAlchemy ORM
- Alembic for migrations
- Celery + Redis for async tasks
- OpenAI / Anthropic API support
- Docker for local and cloud deployment

---

## What's Already Done

✅ **Environment + Configuration**
- `.env` file created with `DATABASE_URL`, `SECRET_KEY`, etc.
- `pydantic-settings` used to load config dynamically in `config.py`

✅ **Database + ORM**
- SQLAlchemy models defined for:
  - `users`
  - `user_configurations`
  - `system_configurations`
  - `requests`
  - `user_sessions` ✅ NEW
- Alembic set up:
  - Initial migration complete
  - User session table migration complete

✅ **FastAPI App + Auth System**
- FastAPI app started in `main.py`
- `/auth/register` and `/auth/login` endpoints implemented
- Passwords hashed with bcrypt
- JWTs generated and verified with `python-jose`
- Login tokens hashed and persisted in `user_sessions` table
- Swagger UI works at `/docs`

---

## File/Folder Structure

project_root/
├── alembic/
│ ├── versions/
│ └── env.py
├── app/
│ ├── init.py
│ ├── main.py # FastAPI entrypoint
│ ├── config.py # Loads settings from .env
│ ├── database.py # DB engine, session factory
│ ├── api/
│ │ └── auth.py # Auth routes
│ ├── schemas/
│ │ └── auth_schemas.py # Pydantic models for register/login
│ ├── services/
│ │ └── auth_service.py # Auth logic (hashing, JWT, current user)
│ ├── models/
│ │ ├── init.py
│ │ ├── users.py
│ │ ├── user_configurations.py
│ │ ├── system_configurations.py
│ │ ├── requests.py
│ │ └── user_sessions.py # NEW: stores login token hashes
├── .env
├── .gitignore
├── README.md
└── requirements.txt


---

## Defined Classes and Functions

### `app/config.py`
- `Settings(BaseSettings)`: Loads all environment variables
- `settings`: Global instance of `Settings`

### `app/database.py`
- `engine`: SQLAlchemy engine from `DATABASE_URL`
- `SessionLocal`: Session factory
- `Base`: Declarative base

### `app/main.py`
- `app`: FastAPI instance
- Includes routes from `auth.py`

### `app/api/auth.py`
- `register(payload: UserRegister)`: Registers a user (placeholder logic)
- `login(payload: UserLogin)`: Logs in a user, returns JWT

### `app/schemas/auth_schemas.py`
- `UserRegister`: Validates email + password for register
- `UserLogin`: Validates email + password for login

### `app/services/auth_service.py`
- `hash_password(password)`: Hashes password using bcrypt
- `verify_password(password, hashed)`: Verifies hashed password
- `create_token(user_id)`: Issues JWT token
- `get_current_user(token)`: Validates JWT and returns `user_id`
- `register_user(payload)`: Placeholder — just returns hash for now
- `login_user(payload)`: Issues token, stores hashed token in DB

### `app/models/user_sessions.py`
- `UserSession`: SQLAlchemy model for storing user_id, token_hash, expiry, created_at

---

## What’s Next
🔜 In the next session, we will:
1. Add real user registration with email uniqueness + DB lookup
2. Validate password on login
3. Implement logout & token revocation
4. Build `GET /auth/me` to return current logged-in user
5. Write tests for auth flow

---

> ✅ Please upload this `current_context.md` with every new session to continue where we left off.
