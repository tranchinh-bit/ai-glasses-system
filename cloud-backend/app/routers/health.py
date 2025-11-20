import time

from fastapi import APIRouter

from ..schemas import HealthStatus

router = APIRouter(tags=["health"])

_start_time = time.time()


@router.get("/health", response_model=HealthStatus)
async def health():
    uptime = int(time.time() - _start_time)
    return HealthStatus(
        status="ok",
        uptime_sec=uptime,
        version="1.0.0",
    )
