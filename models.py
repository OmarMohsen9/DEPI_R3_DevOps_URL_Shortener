from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    long_url = Column(String(512), index=True, nullable=False)
    clicks = Column(Integer, default=0)  # ✅ For analytics / Prometheus
    created_at = Column(DateTime, default=datetime.utcnow)


class LookupFailure(Base):
    __tablename__ = "lookup_failures"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

