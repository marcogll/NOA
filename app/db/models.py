from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True)
    name = Column(String)
    industry = Column(String)
    social_media = Column(String)
    problem = Column(String)
    sentiment = Column(String)
    intent = Column(String)
    lead_score = Column(Float)
    recommended_service = Column(String)

    # Timestamps in UTC
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
