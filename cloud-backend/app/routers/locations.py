from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..deps import get_db_session

router = APIRouter(
    prefix="/api/v1/location",
    tags=["location"],
)


@router.post("/update", response_model=dict)
async def update_location(
    payload: schemas.LocationUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    stmt = select(models.Location).where(
        models.Location.device_id == payload.device_id
    )
    result = await db.execute(stmt)
    loc = result.scalar_one_or_none()

    if loc is None:
        loc = models.Location(device_id=payload.device_id)
        db.add(loc)

    loc.lat = payload.lat
    loc.lon = payload.lon
    loc.accuracy_m = payload.accuracy_m
    loc.speed_mps = payload.speed_mps
    loc.bearing_deg = payload.bearing_deg
    loc.from_mobile_gps = 1 if payload.from_mobile_gps else 0

    await db.commit()
    return {"status": "ok"}


@router.get("/latest", response_model=schemas.LocationWithMeta)
async def get_latest_location(
    device_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    stmt = select(models.Location).where(
        models.Location.device_id == device_id
    )
    result = await db.execute(stmt)
    loc = result.scalar_one_or_none()

    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return loc
