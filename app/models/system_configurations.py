# system_configurations.py
# Stores global platform configuration options

import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class SystemConfiguration(Base):
    __tablename__ = "system_configurations"

    id = Column(Integer, primary_key=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
