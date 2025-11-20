from __future__ import annotations

from typing import Dict, List

import math


class FusionEngine:
    """
    Gắn camera kép + thông tin depth thành góc toàn cục và distance.

    Sử dụng:
      - map x pixel -> global angle (0..180)
      - lấy median depth trong bbox
    """

    def __init__(self, global_fov_deg: float = 140.0, global_margin_deg: float = 20.0):
        self.global_fov_deg = global_fov_deg
        self.global_margin_deg = global_margin_deg

    def _map_to_global_angle(self, x: float, width: float, is_left: bool) -> float:
        half_fov = self.global_fov_deg / 2.0  # 70°
        base = self.global_margin_deg
        if is_left:
            return base + (x / width) * half_fov
        else:
            return base + half_fov + (x / width) * half_fov

    def fuse_detections(
        self,
        left_dets: List[Dict],
        right_dets: List[Dict],
    ) -> List[Dict]:
        """
        Mỗi detection: {x, y, w, h, label, conf, depth_m, is_left}
        Trả về list objects đã có angle_deg, distance_m.
        """
        fused: List[Dict] = []
        for det in left_dets + right_dets:
            width = det.get("frame_width", 640)
            x_center = det["x"] + det["w"] / 2.0
            angle = self._map_to_global_angle(
                x_center, width, is_left=det.get("is_left", True)
            )
            fused.append(
                {
                    "label": det["label"],
                    "confidence": float(det["conf"]),
                    "distance_m": float(det.get("depth_m", 3.0)),
                    "angle_deg": angle,
                    "is_moving": bool(det.get("is_moving", False)),
                }
            )
        return fused
