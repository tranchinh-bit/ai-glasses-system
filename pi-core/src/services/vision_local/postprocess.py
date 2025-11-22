from typing import Any, Dict, List


def yolo_postprocess(raw_output: Any, conf_threshold: float = 0.3) -> List[Dict[str, Any]]:
    """
    Khung postprocess YOLO – sẽ tuỳ model mà implement.
    Hiện tại trả list rỗng cho an toàn.
    """
    return []
