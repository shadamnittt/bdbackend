from pydantic import BaseModel


class ClinicBase(BaseModel):
    name: str
    address: str | None = None
    phone: str | None = None


class ClinicOut(ClinicBase):
    id: int

    class Config:
        from_attributes = True  # в Pydantic v2 вместо orm_mode


class ClinicUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
