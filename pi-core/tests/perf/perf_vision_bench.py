from pathlib import Path
import time

from ...src.core.fusion_engine import FusionEngine
from ...src.core.events import VisionFrameEvent
from ...src.services.vision_object_danger.danger_analyzer import DangerAnalyzer


def main():
    root = Path(__file__).resolve().parents[2]
    engine = FusionEngine()
    analyzer = DangerAnalyzer(root)
    import asyncio
    asyncio.run(analyzer.init())

    # giả lập 100 frame với 5 object
    frame = VisionFrameEvent(
        frame_id=1,
        detections=[
            {
                "label": "car",
                "confidence": 0.8,
                "distance_m": 3.0,
                "angle_deg": 90.0,
            }
        ],
    )

    start = time.time()
    n = 200
    for i in range(n):
        frame.frame_id = i
        hazards = analyzer.analyze(frame)
    dur = time.time() - start
    print(f"{n} frames analyzed in {dur:.3f}s -> {n/dur:.1f} FPS")


if __name__ == "__main__":
    main()
