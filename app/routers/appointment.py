# app/routers/appointment.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.appointment_schemas import AppointmentCreate, AppointmentOut, AppointmentUpdate
from app.crud.appointment_crud import create_appointment, get_appointments, update_appointment, delete_appointment
from app.database import get_db

router = APIRouter(
    prefix="/appointments",
    tags=["Записи клиентов"]
)

@router.post("/", response_model=AppointmentOut)
def add_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return create_appointment(db, appointment)

@router.get("/", response_model=List[AppointmentOut])
def list_appointments(q: str = Query("", description="Поиск по клиенту или причине"), db: Session = Depends(get_db)):
    return get_appointments(db, q)

@router.put("/{appointment_id}", response_model=AppointmentOut)
def edit_appointment(appointment_id: int, appointment: AppointmentUpdate, db: Session = Depends(get_db)):
    updated = update_appointment(db, appointment_id, appointment)
    if updated is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return updated

@router.delete("/{appointment_id}")
def remove_appointment(appointment_id: int, db: Session = Depends(get_db)):
    deleted = delete_appointment(db, appointment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return {"detail": "Запись удалена"}
