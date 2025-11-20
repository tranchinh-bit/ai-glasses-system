from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func

from .database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), index=True, nullable=False)

    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    accuracy_m = Column(Float)
    speed_mps = Column(Float)
    bearing_deg = Column(Float)
    from_mobile_gps = Column(Integer)  # 0/1

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), index=True, nullable=False)

    hazard_code = Column(String(64))
    severity = Column(String(32))
    title = Column(String(255))
    message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
