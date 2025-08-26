# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from typing import List

# from app.schemas.appointment_schemas import AppointmentCreate, AppointmentOut, AppointmentUpdate
# from app.crud.appointment_crud import create_appointment, get_appointments, update_appointment, delete_appointment
# from app.database import get_db
# from app.models.user import User
# from app.dependencies import get_current_user


# router = APIRouter(
#     prefix="/appointments",
#     tags=["Записи клиентов"]
# )


# @router.post("/", response_model=AppointmentOut)
# def add_appointment(
#     appointment: AppointmentCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     if current_user.role.lower() == "doctor":
#         doctor_id = current_user.id
#     else:
#         # админ/регистратор должны явно указать врача
#         if not appointment.doctor_id:
#             raise HTTPException(status_code=400, detail="Нужно указать врача")
#         doctor_id = appointment.doctor_id

#     return create_appointment(db, appointment, doctor_id)


# @router.get("/", response_model=List[AppointmentOut])
# def list_appointments(
#     q: str = Query("", description="Поиск по клиенту или причине"),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     if current_user.role.lower() == "doctor":
#         # врачи видят только свои записи
#         return get_appointments(db, q, doctor_id=current_user.id)
#     return get_appointments(db, q)


# @router.put("/{appointment_id}", response_model=AppointmentOut)
# def edit_appointment(
#     appointment_id: int,
#     appointment: AppointmentUpdate,
#     db: Session = Depends(get_db)
# ):
#     updated = update_appointment(db, appointment_id, appointment)
#     if updated is None:
#         raise HTTPException(status_code=404, detail="Запись не найдена")
#     return updated


# @router.delete("/{appointment_id}")
# def remove_appointment(appointment_id: int, db: Session = Depends(get_db)):
#     deleted = delete_appointment(db, appointment_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Запись не найдена")
#     return {"detail": "Запись удалена"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.appointment_schemas import AppointmentCreate, AppointmentOut, AppointmentUpdate
from app.crud.appointment_crud import create_appointment, get_appointments, update_appointment, delete_appointment
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/appointments",
    tags=["Записи клиентов"]
)

@router.post("/", response_model=AppointmentOut)
def add_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Если текущий пользователь врач — устанавливаем его ID
    if current_user.role.lower() == "doctor":
        appointment.doctor_id = current_user.id
    else:
        # админ/регистратор должны явно указать врача
        if not appointment.doctor_id:
            raise HTTPException(status_code=400, detail="Нужно указать врача")

    return create_appointment(db, appointment)


@router.get("/", response_model=List[AppointmentOut])
def list_appointments(
    q: str = Query("", description="Поиск по клиенту или причине"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() == "doctor":
        # врачи видят только свои записи
        return get_appointments(db, q, doctor_id=current_user.id)
    return get_appointments(db, q)


@router.put("/{appointment_id}", response_model=AppointmentOut)
def edit_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db)
):
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
