# app/schemas/user_schema.py
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True  # вместо orm_mode для Pydantic v2
