import asyncio
import time
from typing import Any

import psutil
from loguru import logger

from src.utils.event_bus import EventBus
from src.core.mode_manager import ModeManager
from src.services.power_manager.power_manager import PowerManager


class HealthDaemon:
    def __init__(self, event_bus: EventBus, mode_manager: ModeManager, power_manager: PowerManager):
        self.event_bus = event_bus
        self.mode_manager = mode_manager
        self.power_manager = power_manager

    async def run(self) -> None:
        while True:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            temp = 0.0
            try:
                temps = psutil.sensors_temperatures()
                for key, val in temps.items():
                    if val:
                        temp = val[0].current
                        break
            except Exception:
                pass

            self.power_manager.update_profile_by_battery()

            health = {
                "cpu_usage": cpu,
                "mem_usage": mem,
                "temperature_c": temp,
                "battery_percent": psutil.sensors_battery().percent if psutil.sensors_battery() else -1,
                "offload_mode": self.mode_manager.get_current_mode(),
                "power_profile": self.power_manager.get_profile_name(),
                "network_status": "TODO",  # có thể gắn logic sau
                "ts": int(time.time() * 1000),
            }

            logger.debug(f"[HEALTH] {health}")
            await self.event_bus.publish("health_tick", health)

            await asyncio.sleep(5.0)
