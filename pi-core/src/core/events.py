from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class VisionFrameEvent:
    frame_id: int
    detections: List[Dict[str, Any]]  # mỗi detection: label, conf, dist, angle


@dataclass
class HazardEvent:
    hazard_code: str
    severity: str
    message: str
    related_objects: List[Dict[str, Any]]


@dataclass
class PowerProfileChangedEvent:
    profile_name: str
