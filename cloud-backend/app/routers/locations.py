from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas
from ..deps import get_db
from ..ws.family_ws import ws_manager  # để broadcast realtime

router = APIRouter(prefix="/api/v1/location", tags=["location"])


@router.post("/update", response_model=schemas.LocationOut)
def update_location(payload: schemas.LocationCreate, db: Session = Depends(get_db)):
    # ensure device exists
    device = db.get(models.Device, payload.device_id)
    if device is None:
        device = models.Device(id=payload.device_id, name=None)
        db.add(device)
        db.flush()

    loc = models.Location(
        device_id=payload.device_id,
        lat=payload.lat,
        lon=payload.lon,
        accuracy_m=payload.accuracy_m,
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)

    # broadcast qua WebSocket cho family app
    ws_manager.broadcast_location(loc)

    return loc


@router.get("/latest", response_model=schemas.LocationOut)
def get_latest_location(
    device_id: str = Query(...),
    db: Session = Depends(get_db),
):
    q = (
        db.query(models.Location)
        .filter(models.Location.device_id == device_id)
        .order_by(models.Location.created_at.desc())
    )
    loc = q.first()
    if not loc:
        raise HTTPException(status_code=404, detail="No location for this device")
    return loc


@router.get("/history", response_model=List[schemas.LocationOut])
def get_location_history(
    device_id: str = Query(...),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    q = (
        db.query(models.Location)
        .filter(models.Location.device_id == device_id)
        .order_by(models.Location.created_at.desc())
        .limit(limit)
    )
    return list(q)
