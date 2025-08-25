from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)   # ✅ добавляем
    clinic_name = Column(String, nullable=True) # ✅ у тебя тоже есть в схемах
    role = Column(String, default="registrar")
    hashed_password = Column(String, nullable=False)

    clients = relationship("Client", back_populates="user", cascade="all, delete-orphan")
    clinic_id = Column(Integer, ForeignKey("clinic_profile.id"), nullable=True)

    clinic = relationship("ClinicProfile", back_populates="users")

