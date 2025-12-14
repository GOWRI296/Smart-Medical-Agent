# backend/app/models/appointment.py

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    reason = Column(String, nullable=True)
    symptoms = Column(String, nullable=True)  # LLM can store comma-separated tags

    calendar_event_id = Column(String, nullable=True)
    status = Column(String, default="scheduled")  # scheduled/cancelled/completed

    doctor = relationship("Doctor")
    patient = relationship("Patient")
