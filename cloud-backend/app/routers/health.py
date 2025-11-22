from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..deps import get_db
from ..schemas import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
def health_check(db: Session = Depends(get_db)):
    # simple db check
    try:
        db.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "error"

    return HealthStatus(status="ok", database=db_status, time=datetime.utcnow())
