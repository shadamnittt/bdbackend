from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class ClinicProfile(Base):
    __tablename__ = "clinic_profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)          # Название клиники
    address = Column(String, nullable=False)       # Адрес
    phone = Column(String, nullable=True)          # Телефон
    email = Column(String, nullable=True)          # Email
    description = Column(Text, nullable=True)      # Описание
    logo_url = Column(String, nullable=True)       # Логотип (ссылка на файл)

    # 🔗 Связи
    users = relationship("User", back_populates="clinic", cascade="all, delete")
    clients = relationship("Client", back_populates="clinic", cascade="all, delete")
    doctors = relationship("Doctor", back_populates="clinic", cascade="all, delete")

