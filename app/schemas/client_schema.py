from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    full_name: str
    phone_number: str
    status: str  # например, "надежный" или "проблемный"
    comment: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int
    date_created: datetime
    user_id: int

    class Config:
        orm_mode = True