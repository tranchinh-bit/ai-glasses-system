from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


# ====== Device ======

class DeviceBase(BaseModel):
    id: str = Field(..., description="device_id của kính / app")
    name: Optional[str] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceOut(DeviceBase):
    created_at: datetime

    class Config:
        from_attributes = True


# ====== Location ======

class LocationBase(BaseModel):
    device_id: str
    lat: float
    lon: float
    accuracy_m: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class LocationOut(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ====== Alert ======

class AlertBase(BaseModel):
    device_id: str
    level: str = Field(..., description="INFO/LOW/MEDIUM/HIGH/CRITICAL")
    type: Optional[str] = Field(default=None, description="danger/sos/health/...")
    message: str
    rule_id: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertOut(AlertBase):
    id: int
    created_at: datetime
    handled: bool

    class Config:
        from_attributes = True


# ====== Health ======

class HealthStatus(BaseModel):
    status: str = "ok"
    database: str = "ok"
    time: datetime
