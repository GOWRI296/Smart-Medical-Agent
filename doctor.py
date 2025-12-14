# backend/app/models/doctor.py

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialization = Column(String, nullable=True)
    timezone = Column(String, default="Asia/Kolkata")

    google_calendar_connected = Column(Boolean, default=False)
    google_oauth_token = Column(String, nullable=True)  # encrypted later
