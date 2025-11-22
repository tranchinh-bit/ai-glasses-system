from dataclasses import dataclass
from typing import Any


@dataclass
class DangerEvent:
    level: str
    message: str
    rule_id: str
    timestamp_ms: int


@dataclass
class HealthEvent:
    cpu_usage: float
    mem_usage: float
    temperature_c: float
    battery_percent: float
    offload_mode: str
    power_profile: str
    network_status: str


@dataclass
class ModeChangeEvent:
    old_mode: str
    new_mode: str
    reason: str


@dataclass
class FrameProcessedEvent:
    fps: float
    offload_used: bool
    extra: Any = None
