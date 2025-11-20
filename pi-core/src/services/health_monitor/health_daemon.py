from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, Any

from ...utils.logging_util import setup_logger
from ...utils.config_loader import ConfigLoader
from ...utils.event_bus import EventBus


class HealthDaemon:
    def __init__(self, bus: EventBus, config_loader: ConfigLoader) -> None:
        self._bus = bus
        self._cfg = config_loader.load("system")
        self._logger = setup_logger("HealthDaemon",
                                    Path("data/logs/health.log"))
        self._task: asyncio.Task | None = None

    async def init(self) -> None:
        interval = self._cfg.get("heartbeat_interval_sec", 20)
        self._task = asyncio.create_task(self._loop(interval))

    async def _loop(self, interval: int) -> None:
        while True:
            await asyncio.sleep(interval)
            await self._report_health()

    async def _report_health(self) -> None:
        # đơn giản: log; sau có thể publish event hoặc gửi backend
        stats: Dict[str, Any] = {}
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                t = int(f.read().strip())
                stats["cpu_temp_c"] = t / 1000.0
        except Exception:
            pass
        self._logger.info("Health: %s", stats)
