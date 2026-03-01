from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum

from .db import Base


class Level(str, PyEnum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class AlertEntry(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    level = Column(Enum(Level), index=True)
    message = Column(String, index=True)
