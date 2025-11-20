from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List

from ..utils.config_loader import ConfigLoader
from ..utils.event_bus import EventBus
from ..utils.logging_util import setup_logger
from .mode_manager import ModeManager
from .events import VisionFrameEvent, HazardEvent
from ..services.vision_object_danger.detector import Detector
from ..services.vision_object_danger.danger_analyzer import DangerAnalyzer
from ..services.io_hub.ws_client import WsClient
from ..services.power_manager.power_manager import PowerManager
from ..services.health_monitor.health_daemon import HealthDaemon


class Orchestrator:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.config_loader = ConfigLoader(root_dir / "configs")
        self.bus = EventBus()
        self.logger = setup_logger("Orchestrator", root_dir / "data/logs/core.log")

        self.mode_manager = ModeManager(self.bus, self.config_loader)
        self.detector = Detector(root_dir)
        self.danger_analyzer = DangerAnalyzer(root_dir)
        self.ws_client = WsClient(self.bus, self.config_loader)
        self.power_manager = PowerManager(self.bus, self.config_loader)
        self.health_daemon = HealthDaemon(self.bus, self.config_loader)

    async def init(self) -> None:
        await self.mode_manager.init()
        await self.ws_client.init()
        await self.power_manager.init()
        await self.health_daemon.init()
        await self.detector.init()
        await self.danger_analyzer.init()

        # subscribe events
        await self.bus.subscribe("vision_frame", self._on_vision_frame)
        await self.bus.subscribe("hazard", self._on_hazard)

    async def _on_vision_frame(self, _type: str, event: VisionFrameEvent) -> None:
        hazards: List[HazardEvent] = self.danger_analyzer.analyze(event)
        for hz in hazards:
            await self.bus.publish("hazard", hz)

    async def _on_hazard(self, _type: str, event: HazardEvent) -> None:
        # gửi hazard lên mobile/backend qua WS
        await self.ws_client.send_hazard(event)

    async def run(self) -> None:
        self.logger.info("Starting main loop...")
        await self.detector.run(self.bus)
