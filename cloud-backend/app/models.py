from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)  # device_id từ Pi / App
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    locations = relationship("Location", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device", cascade="all, delete-orphan")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    accuracy_m = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    device = relationship("Device", back_populates="locations")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    level = Column(String, nullable=False)        # INFO / LOW / MEDIUM / HIGH / CRITICAL
    type = Column(String, nullable=True)          # "danger", "sos", ...
    message = Column(Text, nullable=False)
    rule_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    handled = Column(Boolean, default=False)

    device = relationship("Device", back_populates="alerts")
