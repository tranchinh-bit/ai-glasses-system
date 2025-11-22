from typing import List, Dict, Any


class FusionEngine:
    """
    Ghép kết quả vision + depth + face.
    Ở đây chỉ là khung, sau này bạn có thể cài logic chi tiết.
    """

    def __init__(self, vision_labels: Dict[int, Dict[str, Any]] | None = None):
        self.vision_labels = vision_labels or {}

    def fuse(self, detections: List[Dict[str, Any]], depth_info=None, face_info=None) -> List[Dict[str, Any]]:
        # Hiện tại chỉ trả lại detections, sau này có thể chỉnh sửa:
        # - thêm distance từ depth
        # - thêm recognized_name từ face
        fused = []
        for d in detections:
            fused.append(d)
        return fused
