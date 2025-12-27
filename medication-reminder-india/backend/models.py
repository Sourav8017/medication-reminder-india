from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    medications = relationship("UserMedication", back_populates="user")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    condition = Column(String, nullable=False)
    medicine_type = Column(String, nullable=False)   # chronic / acute
    risk_if_missed = Column(String, nullable=False)  # low / medium / high / very_high

    users = relationship("UserMedication", back_populates="medicine")


class UserMedication(Base):
    __tablename__ = "user_medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))

    dosage = Column(String, nullable=False)
    frequency_per_day = Column(Integer, nullable=False)

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="medications")
    medicine = relationship("Medicine", back_populates="users")
    logs = relationship("MedicationLog", back_populates="user_medicine")


class MedicationLog(Base):
    __tablename__ = "medication_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_medication_id = Column(Integer, ForeignKey("user_medications.id"))

    scheduled_time = Column(DateTime, nullable=False)
    taken = Column(Boolean, default=False)

    logged_at = Column(DateTime, default=datetime.utcnow)

    user_medicine = relationship("UserMedication", back_populates="logs")
