# Object Detection Model Spec

- Task: Real-time object detection on Pi Zero 2W.
- Backbone: YOLO nano variant (e.g., YOLOv5n / YOLOv8n custom).
- Input size: 320x320
- Format: TFLite INT8 with full integer quantization.
- Classes:
  - person, motorbike, car, bus, truck, bicycle, dog
  - pole, trash_can, door, stairs_up, stairs_down
  - curb_up, curb_down
  - traffic_light, traffic_sign, crosswalk, lane_mark
- Inference threads: 2–3 (tuned per benchmark).
- Target latency: < 120 ms per frame on Pi Zero 2W.
