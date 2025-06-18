# Phase 1: Core Infrastructure - Database Setup

## Goal
Establish the foundational PostgreSQL database schema using SQLAlchemy ORM with migrations.

## Prerequisites
- PostgreSQL 15+
- Python 3.11+
- SQLAlchemy ORM
- Alembic for migrations

## Implementation Steps

### Step 1: Install Dependencies
```bash
pip install sqlalchemy psycopg2-binary alembic
```

### Step 2: Configure Database Connection
In `app/config.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

In `app/database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Step 3: Define Models
Create `app/models/` with the following SQLAlchemy models:

#### `users.py`
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    subscription_tier = Column(String(50), default="free")
    api_quota_daily = Column(Integer, default=5)
    api_quota_used_today = Column(Integer, default=0)
    quota_reset_date = Column(Date, default=datetime.date.today)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
```

(Repeat similar for `user_configurations.py`, `system_configurations.py`, `requests.py`, etc.)

### Step 4: Setup Alembic for Migrations
```bash
alembic init alembic
```
Edit `alembic.ini` and `env.py` to point to your `DATABASE_URL` and metadata.

Generate migrations:
```bash
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

### Step 5: Test Schema
Use `psql` or DB viewer to confirm tables are created.

## Completion Criteria
- [x] Database running locally
- [x] All core tables exist (`users`, `requests`, etc.)
- [x] Alembic setup with initial migration applied

## Notes
- Foreign keys should use `ON DELETE CASCADE`
- Use `DateTime.utcnow` for `created_at` and `updated_at`
- Add indexes on `user_id` for filtering and performance

---

> **Next: Build the FastAPI app structure and connect it to this DB using dependency injection.**
