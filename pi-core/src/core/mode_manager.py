import time
from typing import Dict
from loguru import logger


class ModeManager:
    """
    Quyết định OFFLOAD mode hiện tại dựa trên:
    - Cấu hình (system.yaml).
    - Trạng thái kết nối phone (ws_client).
    - Power profile / nhiệt độ.
    """

    def __init__(self, system_cfg: Dict, power_profiles: Dict):
        self.system_cfg = system_cfg
        self.power_profiles_cfg = power_profiles
        self.base_mode = system_cfg.get("offload_mode", "AUTO")
        self.current_mode = self.base_mode
        self.last_phone_seen_ts = 0.0
        self.phone_heartbeat_timeout = system_cfg.get("network", {}) \
            .get("phone_heartbeat_timeout_sec", 10)

    def notify_phone_alive(self) -> None:
        self.last_phone_seen_ts = time.time()

    def _is_phone_alive(self) -> bool:
        if self.last_phone_seen_ts <= 0:
            return False
        return (time.time() - self.last_phone_seen_ts) < self.phone_heartbeat_timeout

    def decide_mode(self) -> str:
        """
        Gọi định kỳ (ví dụ mỗi vài giây) để cập nhật current_mode.
        """
        if self.base_mode == "LOCAL":
            self.current_mode = "LOCAL"
        elif self.base_mode == "PHONE":
            # PHONE nhưng nếu phone chết thì fallback LOCAL
            if self._is_phone_alive():
                self.current_mode = "PHONE"
            else:
                self.current_mode = "LOCAL"
        else:  # AUTO
            if self._is_phone_alive():
                self.current_mode = "PHONE"
            else:
                self.current_mode = "LOCAL"

        return self.current_mode

    def set_base_mode(self, mode: str) -> None:
        logger.info(f"Base offload mode changed from {self.base_mode} to {mode}")
        self.base_mode = mode

    def get_current_mode(self) -> str:
        return self.current_mode
