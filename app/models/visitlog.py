from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class VisitLog(Base):
    __tablename__ = "visitlogs"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    date = Column(DateTime)
    status_on_visit = Column(Text)  # Можно сделать просто String, если коротко
    comment = Column(Text, nullable=True)

    client = relationship("Client", back_populates="visit_logs")
    

