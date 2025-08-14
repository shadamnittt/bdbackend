# app/crud/appointment_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.appointment import Appointment
from app.models.client import Client
from app.schemas.appointment_schemas import AppointmentCreate, AppointmentUpdate
from datetime import datetime

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(
        client_id=appointment.client_id,
        date_time=appointment.date_time or datetime.utcnow(),
        reason=appointment.reason,
        comment=appointment.comment
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session, q: str = ""):
    query = db.query(Appointment).join(Appointment.client)
    if q:
        like_q = f"%{q}%"
        query = query.filter(
            or_(
                Client.full_name.ilike(like_q),
                Appointment.reason.ilike(like_q)
            )
        )
    return query.order_by(Appointment.date_time.desc()).all()

def update_appointment(db: Session, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        return None
    for field, value in appointment.dict(exclude_unset=True).items():
        setattr(db_appointment, field, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not db_appointment:
        return None
    db.delete(db_appointment)
    db.commit()
    return True
