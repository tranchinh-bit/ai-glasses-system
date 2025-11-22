
---

### `docs/03-pi-vision-algorithms.md`

```markdown
# 03 – Pi Vision Algorithms

## 1. Mục tiêu

- Chạy được trên **Raspberry Pi Zero 2W** (CPU ARM Cortex-A53, RAM hạn chế).
- Vẫn đảm bảo:
  - Phát hiện chướng ngại trước mặt.
  - Cảnh báo phương tiện lao tới (xe máy, ô tô).
  - Hỗ trợ nhận diện mặt người quen (nếu bật).
- Tối ưu: dùng **model INT8**, pipeline C++ + Python phối hợp.

## 2. Pipeline tổng quan trên Pi

### 2.1. Thành phần chính

- `camera_service` (C++, libcamera):  
  - Captures 2 camera (dual cam) → ghép FOV ~140°.
  - Chuyển frame sang Python qua socket/IPC.

- `vision_local/engine.py` (Python):
  - Tải `yolo_v8n_int8.tflite`.
  - Tiền xử lý, hậu xử lý bounding boxes.

- `vision_object_danger/` (C++):
  - `detector.cpp`: logic đánh giá object nguy hiểm.
  - `tracker.cpp`: theo dõi object qua nhiều frame.
  - `danger_analyzer.cpp`: đánh giá mức độ nguy hiểm (rules).

- `core/fusion_engine.py`:
  - Kết hợp detection + depth + face + rule.

### 2.2. Luồng xử lý cơ bản (LOCAL mode)

1. Camera chụp frame (720p → resize 320x320/416x416).
2. Vision engine TFLite chạy inference → danh sách bbox.
3. Depth-lite model (nếu bật) hoặc stereo depth estimate → distance.
4. Face recognition (nếu bật):
   - Crop mặt → embed → so sánh với database `data/faces/*.npy`.
5. Fusion + Danger Analyzer:
   - Ghép thông tin object + distance + velocity → đánh giá nguy hiểm.
6. Output:
   - Gửi `DangerAlert` + TTS trên Pi.
   - Gửi event lên phone/cloud (nếu có kết nối).

## 3. YOLOv8n INT8 trên Pi

### 3.1. Model

- `models/yolo_v8n_int8.tflite`
- Input: 320x320 hoặc 416x416 BGR/RGB.
- Output: tensor chứa [x, y, w, h, score, class].

### 3.2. Tối ưu

- Sử dụng **TFLite runtime** (không cần full TensorFlow).
- Dùng **single-thread** hoặc tối đa 2 thread (tuỳ benchmark).
- Giảm FPS nếu quá tải: 5–10 fps là đủ.

Pseudo-code:

```python
# engine.py
class TFLiteYoloEngine:
    def __init__(self, model_path, max_fps):
        self.interpreter = tflite.Interpreter(model_path=model_path, num_threads=2)
        self.interpreter.allocate_tensors()
        self.last_infer_ts = 0
        self.max_fps = max_fps

    def infer(self, frame_bgr) -> List[DetectionItem]:
        now = time.time()
        if now - self.last_infer_ts < 1.0 / self.max_fps:
            return []  # skip để tiết kiệm CPU
        self.last_infer_ts = now

        # preprocess, set tensor, invoke, get output, postprocess...
        return detections
