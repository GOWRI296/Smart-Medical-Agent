# backend/app/routes/appointments.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = Appointment(
        doctor_id=data.doctor_id,
        patient_id=data.patient_id,
        start_time=data.start_time,
        end_time=data.end_time,
        reason=data.reason,
        symptoms=data.symptoms
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: UUID, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()
