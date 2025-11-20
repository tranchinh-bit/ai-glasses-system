from datetime import datetime
from pydantic import BaseModel


class LocationUpdate(BaseModel):
    device_id: str
    lat: float
    lon: float
    accuracy_m: float | None = None
    speed_mps: float | None = None
    bearing_deg: float | None = None
    from_mobile_gps: bool = False


class LocationWithMeta(LocationUpdate):
    updated_at: datetime


class AlertBase(BaseModel):
    device_id: str
    hazard_code: str | None = None
    severity: str | None = None
    title: str | None = None
    message: str | None = None


class AlertCreate(AlertBase):
    pass


class AlertOut(AlertBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HealthStatus(BaseModel):
    status: str
    uptime_sec: int
    version: str
