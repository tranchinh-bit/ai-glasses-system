import asyncio
from typing import Dict, Any, List

import numpy as np
from loguru import logger

from src.utils.perf_timer import perf_timer
from src.services.power_manager.power_manager import PowerManager
from src.utils.event_bus import EventBus


class LocalVisionEngine:
    """
    Pipeline local: đọc frame từ camera_service (qua IPC),
    chạy TFLite YOLOv8n nếu mode = LOCAL hoặc AUTO nhưng không có phone.
    Ở đây mock đơn giản (chưa nối libcamera thật).
    """

    def __init__(self, camera_cfg: Dict[str, Any], power_manager: PowerManager, event_bus: EventBus, mode_manager):
        self.camera_cfg = camera_cfg
        self.power_manager = power_manager
        self.event_bus = event_bus
        self.mode_manager = mode_manager
        self.running = True

    async def run(self) -> None:
        logger.info("[VISION_LOCAL] started.")
        while self.running:
            mode = self.mode_manager.get_current_mode()
            profile = self.power_manager.get_current_profile()

            if not profile.get("enable_vision_local", True) and mode == "PHONE":
                # Chỉ dùng offload, bỏ qua vision_local
                await asyncio.sleep(0.1)
                continue

            max_fps = self.power_manager.get_max_fps()
            frame_interval = 1.0 / max_fps

            with perf_timer("capture+infer"):
                # TODO: đọc frame từ camera_service IPC, tạm mock = random
                fake_frame = np.zeros((self.camera_cfg["resolution"]["height"],
                                       self.camera_cfg["resolution"]["width"],
                                       3), dtype=np.uint8)
                detections: List[Dict[str, Any]] = []  # TODO: chạy TFLite thực tế

            # TODO: publish event detections để danger_analyzer xử lý
            await asyncio.sleep(frame_interval)
