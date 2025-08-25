from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone_number = Column(String)
    status = Column(String)  # "надежный" или "проблемный"
    comment = Column(Text, nullable=True)
    date_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_blacklisted = Column(Boolean, default=False)  

    user = relationship("User", back_populates="clients")
    visit_logs = relationship("VisitLog", back_populates="client", cascade="all, delete")
    appointments = relationship("Appointment", back_populates="client")
    clinic_id = Column(Integer, ForeignKey("clinic_profile.id"), nullable=True)

    clinic = relationship("ClinicProfile", back_populates="clients")
