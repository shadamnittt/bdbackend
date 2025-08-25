from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    client_id: int
    date_time: datetime
    reason: str
    comment: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    doctor_id: Optional[int] = None   # 👈 теперь можно указывать врача


class AppointmentUpdate(AppointmentBase):
    doctor_id: Optional[int] = None


class AppointmentOut(AppointmentBase):
    id: int
    doctor_id: Optional[int]

    class Config:
        from_attributes = True  # ✅ для работы с SQLAlchemy
