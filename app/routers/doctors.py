from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# ----------------- SCHEMAS -----------------
class DoctorCreate(BaseModel):
    full_name: str
    specialty: str
    phone: Optional[str] = None
    email: Optional[str] = None
    clinic_id: int   # 🔗 к какой клинике врач принадлежит

class DoctorResponse(BaseModel):
    id: int
    full_name: str
    specialty: str
    phone: Optional[str]
    email: Optional[str]
    clinic_id: int

    class Config:
        orm_mode = True


# ----------------- CRUD -----------------
@router.post("/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(
        full_name=doctor.full_name,
        specialty=doctor.specialty,
        phone=doctor.phone,
        email=doctor.email,
        clinic_id=doctor.clinic_id
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@router.get("/", response_model=List[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_doctor.full_name = doctor.full_name
    db_doctor.specialty = doctor.specialty
    db_doctor.phone = doctor.phone
    db_doctor.email = doctor.email
    db_doctor.clinic_id = doctor.clinic_id

    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(db_doctor)
    db.commit()
    return {"detail": "Doctor deleted"}

class AppointmentResponse(BaseModel):
    id: int
    client_id: int
    date_time: str
    reason: str
    comment: Optional[str] = None

    class Config:
        orm_mode = True


@router.get("/{doctor_id}/appointments", response_model=List[AppointmentResponse])
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor.appointments
