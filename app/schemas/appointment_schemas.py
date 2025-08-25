# from pydantic import BaseModel
# from datetime import datetime
# from typing import Optional


# class AppointmentBase(BaseModel):
#     client_id: int
#     date_time: datetime
#     reason: str
#     comment: Optional[str] = None


# class AppointmentCreate(AppointmentBase):
#     doctor_id: Optional[int] = None   # 👈 теперь можно указывать врача


# class AppointmentUpdate(AppointmentBase):
#     doctor_id: Optional[int] = None


# class AppointmentOut(AppointmentBase):
#     id: int
#     doctor_id: Optional[int]

#     class Config:
#         from_attributes = True  # ✅ для работы с SQLAlchemy

# class DoctorOut(BaseModel):
#     id: int
#     full_name: str
#     specialty: str

#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ----- БАЗА -----
class AppointmentBase(BaseModel):
    client_id: int
    date_time: datetime
    reason: str
    comment: Optional[str] = None


# ----- СОЗДАНИЕ -----
class AppointmentCreate(AppointmentBase):
    doctor_id: Optional[int] = None


# ----- ОБНОВЛЕНИЕ -----
class AppointmentUpdate(BaseModel):
    client_id: Optional[int] = None
    date_time: Optional[datetime] = None
    reason: Optional[str] = None
    comment: Optional[str] = None
    doctor_id: Optional[int] = None


# ----- ВРАЧ -----
class DoctorOut(BaseModel):
    id: int
    full_name: str
    specialty: str

    class Config:
        orm_mode = True


# ----- ВЫВОД ЗАПИСЕЙ -----
class AppointmentOut(BaseModel):
    id: int
    client_id: int
    date_time: datetime
    reason: str
    comment: Optional[str] = None
    doctor: Optional[DoctorOut] = None   # 👈 вместо doctor_id теперь врач

    class Config:
        orm_mode = True   # или from_attributes = True
