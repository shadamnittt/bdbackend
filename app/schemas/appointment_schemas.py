# app/schemas/appointment_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentBase(BaseModel):
    client_id: int
    date_time: datetime
    reason: str
    comment: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        from_attributes = True  # pydantic v2 заменяет orm_mode на from_attributes
