from __future__ import annotations

import asyncio
from typing import Dict

from ..utils.logging_util import setup_logger
from ..utils.config_loader import ConfigLoader
from .events import PowerProfileChangedEvent
from ..utils.event_bus import EventBus


class ModeManager:
    def __init__(self, bus: EventBus, config_loader: ConfigLoader) -> None:
        self._bus = bus
        self._config_loader = config_loader
        self._logger = setup_logger("ModeManager")
        self._power_profiles: Dict[str, dict] = {}
        self._current_profile = "balanced"

    async def init(self) -> None:
        self._power_profiles = self._config_loader.load("power_profiles")["profiles"]
        self._current_profile = (
            self._config_loader.load("system").get("power_profile", "balanced")
        )
        await self.apply_power_profile(self._current_profile)

    async def apply_power_profile(self, name: str) -> None:
        if name not in self._power_profiles:
            self._logger.warning("Unknown power profile %s", name)
            return
        self._current_profile = name
        profile = self._power_profiles[name]
        self._logger.info("Applying power profile: %s", name)

        # Ở đây có thể set cpu governor, chỉnh cam fps, v.v.
        # Để đơn giản, ta log + publish event.
        event = PowerProfileChangedEvent(profile_name=name)
        await self._bus.publish("power_profile_changed", event)

    def get_profile(self) -> dict:
        return self._power_profiles.get(self._current_profile, {})
