from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models, schemas
from ..deps import get_db_session
from ..ws.family_ws import broadcast_alert

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["alerts"],
)


@router.post("", response_model=dict)
async def create_alert(
    payload: schemas.AlertCreate,
    db: AsyncSession = Depends(get_db_session),
):
    alert = models.Alert(
        device_id=payload.device_id,
        hazard_code=payload.hazard_code,
        severity=payload.severity,
        title=payload.title,
        message=payload.message,
    )
    db.add(alert)
    await db.commit()
    await db.refresh(alert)

    # gửi realtime cho Family App qua WS
    await broadcast_alert(alert)

    return {"status": "ok"}


@router.get("", response_model=list[schemas.AlertOut])
async def list_alerts(
    device_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(models.Alert)
        .where(models.Alert.device_id == device_id)
        .order_by(models.Alert.id.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    alerts = result.scalars().all()
    return alerts
