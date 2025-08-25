from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)       # ФИО врача
    specialty = Column(String, nullable=False)       # Специальность (например: стоматолог, ортодонт)
    phone = Column(String, nullable=True)            # Телефон (опционально)
    email = Column(String, nullable=True)            # Email (опционально)

    # 🔗 Привязка к клинике
    clinic_id = Column(Integer, ForeignKey("clinic_profile.id"))
    clinic = relationship("ClinicProfile", back_populates="doctors")

    # 🔗 Связь с записями
    appointments = relationship("Appointment", back_populates="doctor")
