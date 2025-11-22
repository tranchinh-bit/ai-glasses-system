from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas
from ..deps import get_db
from ..ws.family_ws import ws_manager

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.post("", response_model=schemas.AlertOut)
def create_alert(payload: schemas.AlertCreate, db: Session = Depends(get_db)):
    device = db.get(models.Device, payload.device_id)
    if device is None:
        device = models.Device(id=payload.device_id, name=None)
        db.add(device)
        db.flush()

    alert = models.Alert(
        device_id=payload.device_id,
        level=payload.level,
        type=payload.type,
        message=payload.message,
        rule_id=payload.rule_id,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    ws_manager.broadcast_alert(alert)

    return alert


@router.get("", response_model=List[schemas.AlertOut])
def list_alerts(
    device_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(models.Alert).order_by(models.Alert.created_at.desc())
    if device_id:
        q = q.filter(models.Alert.device_id == device_id)
    return list(q.limit(limit))
