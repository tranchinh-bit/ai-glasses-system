from __future__ import annotations

import asyncio
from pathlib import Path

from ...utils.logging_util import setup_logger
from ...utils.config_loader import ConfigLoader
from ...utils.event_bus import EventBus
from ...core.events import PowerProfileChangedEvent


class PowerManager:
    def __init__(self, bus: EventBus, config_loader: ConfigLoader):
        self._bus = bus
        self._cfg = config_loader.load("power_profiles")
        self._logger = setup_logger("PowerManager")

    async def init(self) -> None:
        await self._bus.subscribe("power_profile_changed", self._on_profile_changed)

    async def _on_profile_changed(self, _type: str, event: PowerProfileChangedEvent) -> None:
        profile = self._cfg["profiles"].get(event.profile_name)
        if not profile:
            return
        governor = profile.get("cpu_governor")
        if governor:
            await self._set_governor(governor)

    async def _set_governor(self, value: str) -> None:
        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "w") as f:
                f.write(value)
            self._logger.info("Set CPU governor to %s", value)
        except Exception as e:
            self._logger.warning("Failed to set governor: %s", e)
