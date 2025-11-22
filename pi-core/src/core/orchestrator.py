import asyncio
import time
from typing import Dict, Any

from loguru import logger

from src.utils.event_bus import EventBus
from src.utils.config_loader import (
    load_camera_config,
    load_network_config,
    load_audio_config,
    load_security_config,
)
from src.core.mode_manager import ModeManager
from src.services.io_hub.ws_client import WSClient
from src.services.power_manager.power_manager import PowerManager
from src.services.health_monitor.health_daemon import HealthDaemon
from src.services.vision_local.engine import LocalVisionEngine


class Orchestrator:
    def __init__(self, system_cfg: Dict[str, Any], power_profiles_cfg: Dict[str, Any]):
        self.system_cfg = system_cfg
        self.camera_cfg = load_camera_config()
        self.network_cfg = load_network_config()
        self.audio_cfg = load_audio_config()
        self.security_cfg = load_security_config()
        self.power_profiles_cfg = power_profiles_cfg

        self.event_bus = EventBus()
        self.mode_manager = ModeManager(system_cfg, power_profiles_cfg)
        self.power_manager = PowerManager(system_cfg, power_profiles_cfg, self.event_bus)
        self.health_daemon = HealthDaemon(self.event_bus, self.mode_manager, self.power_manager)

        self.ws_client = WSClient(
            self.network_cfg["phone"]["ws_url"],
            self.event_bus,
            self.mode_manager,
            self.security_cfg,
            device_id=system_cfg["device_id"],
        )

        self.local_vision = LocalVisionEngine(
            self.camera_cfg,
            self.power_manager,
            self.event_bus,
            mode_manager=self.mode_manager,
        )

        self._register_handlers()

    def _register_handlers(self) -> None:
        # Khi WSClient nhận heartbeat from phone, nó sẽ trigger event "phone_alive"
        async def on_phone_alive(_payload):
            self.mode_manager.notify_phone_alive()

        self.event_bus.subscribe("phone_alive", on_phone_alive)

    async def run(self) -> None:
        logger.info("Orchestrator starting services...")

        # chạy song song health daemon, ws client, local vision
        tasks = [
            asyncio.create_task(self.health_daemon.run(), name="health_daemon"),
            asyncio.create_task(self.ws_client.run(), name="ws_client"),
            asyncio.create_task(self.local_vision.run(), name="local_vision"),
            asyncio.create_task(self._mode_loop(), name="mode_loop"),
        ]

        await asyncio.gather(*tasks)

    async def _mode_loop(self) -> None:
        """
        Loop đơn giản, định kỳ quyết định mode và thông báo.
        """
        last_mode = None
        while True:
            mode = self.mode_manager.decide_mode()
            if mode != last_mode:
                logger.info(f"[MODE] changed to {mode}")
                last_mode = mode
            await asyncio.sleep(2.0)
