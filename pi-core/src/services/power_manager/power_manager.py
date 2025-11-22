import psutil
from typing import Dict, Any
from loguru import logger

from src.utils.event_bus import EventBus


class PowerManager:
    def __init__(self, system_cfg: Dict[str, Any], power_profiles_cfg: Dict[str, Any], event_bus: EventBus):
        self.system_cfg = system_cfg
        self.profiles_cfg = power_profiles_cfg
        self.event_bus = event_bus
        self.current_profile_name = system_cfg.get("default_power_profile", "BALANCED")
        self.current_profile = self.profiles_cfg["profiles"][self.current_profile_name]

        battery_thr = self.profiles_cfg.get("battery_thresholds", {})
        self.batt_to_low = battery_thr.get("to_low", 20)
        self.batt_to_balanced = battery_thr.get("to_balanced", 40)

    def get_current_profile(self) -> Dict[str, Any]:
        return self.current_profile

    def get_profile_name(self) -> str:
        return self.current_profile_name

    def update_profile_by_battery(self) -> None:
        # RPi Zero 2W không có pin system, nhưng bạn có thể
        # nối với external battery sensor, hoặc tạm dùng psutil (nếu supported).
        batt = psutil.sensors_battery()
        if not batt:
            return

        percent = batt.percent
        if percent < self.batt_to_low and self.current_profile_name != "LOW":
            logger.info(f"[POWER] battery={percent}%, switch to LOW profile")
            self._set_profile("LOW")
        elif percent > self.batt_to_balanced and self.current_profile_name == "LOW":
            logger.info(f"[POWER] battery={percent}%, switch to BALANCED profile")
            self._set_profile("BALANCED")

    def _set_profile(self, name: str) -> None:
        if name not in self.profiles_cfg["profiles"]:
            logger.warning(f"[POWER] profile not found: {name}")
            return
        self.current_profile_name = name
        self.current_profile = self.profiles_cfg["profiles"][name]

    def get_max_fps(self) -> int:
        return int(self.current_profile.get("max_camera_fps", 8))
