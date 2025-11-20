# 03 – Pi Vision Algorithms (Perception Core)

This document describes the key AI algorithms for:

- Object detection
- Danger & obstacle detection
- Traffic context
- OCR (Vietnamese text & numbers)
- Currency recognition (VND)
- Face recognition (known persons)

All are designed for **Raspberry Pi Zero 2W** with TFLite INT8 models where possible.

---

## 1. Camera Pipeline

### 1.1. Frame Capture

- Resolution: 640×480 (configurable).
- Frame rate: ~15 FPS capture.
- Format: RGB24 or YUV → converted to RGB for models.
- `camera_service` writes frames into a ring buffer with capacity ~3–5 frames.
- Vision services always read **the most recent frame**, ignoring backlog.

---

## 2. Object Detection

### 2.1. Model

- Model type: YOLO “nano” variant (e.g., v5n/v8n) → TFLite INT8.
- Input size: 320×320.
- Classes:
  - person, motorbike, car, bus, truck, bicycle, dog,
  - pole, trash_can, door, stairs_up, stairs_down, curb_up, curb_down,
  - traffic_light, traffic_sign, crosswalk, lane_mark, etc.

### 2.2. Preprocessing

1. Resize frame to 320×320.
2. Normalize pixel values to model’s expected range.
3. Optional: dynamic cropping:
   - When in `navigation` mode, emphasize bottom & center of image (ROI).

### 2.3. Postprocessing

1. Run TFLite inference.
2. Apply NMS (IoU threshold ~0.4–0.5).
3. Filter out:
   - Very small boxes (<1% of image area).
   - Low confidence (<0.4–0.5, configurable).

### 2.4. Tracking

Use a lightweight tracker (e.g., SORT/IoU-based):

- Maintain track for each object:
  - ID, class, bounding box, timestamp.
- Update IOU matching between frame t and t+1.
- Tracks lost after N frames without match.

---

## 3. Danger & Obstacle Detection

### 3.1. Distance Approximation

For each tracked object:

- Approximate distance based on:
  - Vertical position (y-coordinate of bbox bottom).
  - Bounding box height.
- Heuristics:
  - Objects closer to the bottom and larger in size → closer.
- Distance categories:
  - `far` ~ >5 m
  - `mid` ~ 2–5 m
  - `near` ~ 0–2 m

### 3.2. Relative Motion & Risk

For each track ID:

- Compute approximate “size velocity”:
  - `dv = bbox_height(t) - bbox_height(t - Δt)`
- If:
  - `distance` is `near` or `mid`, and
  - `dv` is significantly positive over several frames, and
  - object is in `front` area (central horizontal band),
  → classify as **approaching danger**.

### 3.3. Obstacle Rules

Examples:

- If an object is static but in **near + front** region:
  - “Obstacle ahead in about X meters.”
- If approaching object is vehicle/person:
  - “Be careful, a motorbike is moving towards you, about 2 meters ahead.”

### 3.4. Output Event

`danger_analyzer` outputs:

- `DangerEvent` with:
  - `object_class`
  - `direction` (left / right / front)
  - `distance_category`
  - `risk_level` (low/medium/high)

These are consumed by `fusion_engine`.

---

## 4. Traffic Context

### 4.1. Traffic Density

- Count number of vehicles (car, motorbike, bus, truck) within “mid” range.
- `density`:
  - `low`: < 2 vehicles
  - `medium`: 2–5
  - `high`: > 5

### 4.2. Crosswalk

- If object class `crosswalk` is detected in the lower-middle region:
  - Flag `has_crosswalk = true`.

### 4.3. Traffic Lights

1. Detect object `traffic_light`.
2. Crop bounding box → feed to small classifier (Red/Green/Yellow).
3. Output:
   - `light_state: red|green|yellow`.
4. `fusion_engine` can generate:
   - “Đèn đỏ, dừng lại.”
   - “Đèn xanh, có thể qua đường, hãy cẩn thận.”

### 4.4. Lane & Sidewalk Context (optional)

- Simple lane detection via edge & Hough (if cost acceptable) or small segmentation model.
- If user is too close to lane center → “Bạn đang gần làn xe, hãy đi sát lề hơn.”

---

## 5. OCR – Vietnamese Text & Numbers (Left→Right)

### 5.1. Text Detection

- Model: Tiny text detector (EAST/CRAFT-like) → TFLite INT8.
- Input: 320–480 px side.

Outputs: bounding boxes for text regions.

### 5.2. Line Grouping & Sorting

Algorithm:

1. For each bounding box, compute center `(cx, cy)` and vertical span `[y_min, y_max]`.
2. Sort boxes by `cy` (top to bottom).
3. Group boxes into lines:
   - Two boxes are in the same line if their vertical spans overlap significantly (>50%).
4. Within each line, sort by `cx` (left to right).

Result: ordered list of lines, each with ordered list of boxes.

### 5.3. Text Recognition (OCR Engine)

- Use OCR engine with Vietnamese language support.
- For each box (or merged line region):
  - Crop region from original image.
  - Feed into OCR engine.
- Post-process:
  - Normalize spacing.
  - Filter spurious symbols.
  - Optionally expand numbers into spoken Vietnamese (e.g., `120000` → “một trăm hai mươi nghìn”).

### 5.4. Output

`OcrResult`:

- List of lines:
  - `text`
  - optional `bounding_box`
- `fusion_engine` decides how to speak them (line-by-line, with pauses).

---

## 6. Currency Recognition (VND)

### 6.1. Assumptions

- User holds a bill roughly centered & oriented reasonably in front of the camera.
- Triggered by specific “money mode” via voice/remote.

### 6.2. Pipeline

1. Use central crop of frame (e.g., 60–70% of center area).
2. Resize to 224×224.
3. Use TFLite classifier:
   - Classes: `1k`, `2k`, `5k`, `10k`, `20k`, `50k`, `100k`, `200k`, `500k`.
4. Obtain softmax output:
   - Find max probability class.

### 6.3. Decision Logic

- If `max_prob >= 0.9`:
  - Speak: “Tờ tiền X nghìn đồng.”
- Else if `max_prob` in [0.7, 0.9):
  - Speak: “Có vẻ là X nghìn đồng, nhưng không chắc, hãy đưa gần hơn.”
- Else:
  - “Không nhận rõ tờ tiền, hãy chỉnh lại vị trí.”

---

## 7. Face Recognition (Known Persons)

### 7.1. Enrollment

1. User command: “Lưu gương mặt này là [tên].”
2. Face detection on current frame:
   - Use small face detector (e.g., BlazeFace).
3. Capture several clean face crops.
4. For each crop:
   - Resize to 112×112.
   - Run TFLite embedding model (MobileFaceNet).
5. Store embeddings in `faces/<name>/embed_XX.npy`.
6. Update `faces/index.json` with:
   - Name, path, metadata.

### 7.2. Recognition

1. Periodically (e.g., 1–2 FPS) or on-demand:
   - Detect faces in frame.
2. For each face:
   - Generate embedding.
   - Compare with stored embeddings using cosine distance.
3. Matching logic:
   - For each known person:
     - Compute min distance across their embeddings.
   - If best distance < threshold (e.g., 0.8):
     - Recognized as that person.

### 7.3. Output

`FaceRecognizedEvent`:

- `name`
- `direction` (left, right, center)
- `confidence`

`fusion_engine` then speaks:

- “Mẹ đang ở phía trước bên trái.”
- “Anh Nam đang đứng bên phải.”

---

## 8. Performance Considerations

- All vision models:
  - Use TFLite with INT8 quantization where possible.
  - Use `num_threads` tuned for Pi Zero 2W (likely 2–3).
- Avoid:
  - Recreating interpreters on every frame.
  - Copying large arrays multiple times.

Common optimization:

- Pre-allocate input/output tensors.
- Use in-place conversions when possible.
- Reduce FPS adaptively under high CPU load or temperature.

This document must be used as reference when implementing `vision_*` services in `pi-core/src/services/`.
