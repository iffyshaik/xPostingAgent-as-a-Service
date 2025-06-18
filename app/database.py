# app/database.py
# Sets up SQLAlchemy DB engine and session factory

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Create DB engine using URL from .env
engine = create_engine(settings.database_url)

# Create a SessionLocal factory for DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit from
Base = declarative_base()
