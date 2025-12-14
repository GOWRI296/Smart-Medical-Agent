# backend/app/routes/doctors.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter()

@router.post("/", response_model=DoctorResponse)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(
        name=data.name,
        email=data.email,
        specialization=data.specialization,
        timezone=data.timezone
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()
