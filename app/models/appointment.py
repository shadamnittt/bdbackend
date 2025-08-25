# app/models/appointment.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    reason = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    client = relationship("Client", back_populates="appointments")
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    doctor = relationship("Doctor", back_populates="appointments")
