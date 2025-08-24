from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    clinic_name: Optional[str] = None  # можно не присылать

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "registrar"

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True  # Pydantic v2 (аналог orm_mode=True)
        
class UpdateUserRole(BaseModel):
    role: str
