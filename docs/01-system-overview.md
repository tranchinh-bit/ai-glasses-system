# 01 – System Overview

## 1. Mục tiêu dự án

Hệ thống **AI Glasses** hỗ trợ người khiếm thị / thị lực yếu:

- Cảnh báo chướng ngại, phương tiện lao tới.
- Nhận diện ngữ cảnh đời sống (vỉa hè, ổ gà, xe máy, ô tô…).
- Hỗ trợ gọi trợ giúp, chia sẻ vị trí cho người thân.
- Hoạt động mượt trên **Raspberry Pi Zero 2W**, tiết kiệm pin.
- Tận dụng **điện thoại Android** để offload những tác vụ nặng (YOLO, navigation).
- Có **chế độ offline an toàn** khi mất mạng, mất kết nối điện thoại.

## 2. Kiến trúc tổng thể

Hệ thống gồm 3 khối chính:

1. **Pi-Core (Raspberry Pi Zero 2W):**
   - Chạy hệ điều hành Raspberry Pi OS Lite.
   - Gắn trên kính: 2 camera, mic, loa/buzzer, IR remote, nút vật lý.
   - Chạy pipeline vision nhẹ (YOLOv8n-int8, depth-lite), xử lý an toàn cơ bản.
   - Giao tiếp với điện thoại qua **WebSocket** trên Wi-Fi (ưu tiên hotspot từ phone).
   - Gửi heartbeat, health, events (danger, SOS, location) tới phone / cloud.

2. **Mobile Apps:**
   - **User App** (Android – `mobile/user-app`):
     - Kết nối với Pi qua WebSocket.
     - Chạy YOLO nặng hơn trên GPU điện thoại (offload vision).
     - Cung cấp UI cài đặt, quản lý places, faces, profile.
     - Gửi SOS, location lên cloud (nếu bật).
   - **Family App** (Android – `mobile/family-app`):
     - Kết nối với cloud-backend qua WebSocket.
     - Xem vị trí hiện tại/historic của người đeo kính.
     - Nhận cảnh báo nguy hiểm, SOS, health status.

3. **Cloud Backend (tuỳ chọn):**
   - FastAPI + SQLite/Postgres.
   - Nhận location, alerts từ Pi/phone.
   - Lưu trữ lịch sử và broadcast realtime tới family-app.

## 3. Kiến trúc offload Pi–Phone

Có 3 chế độ vận hành chính:

- `LOCAL`: Pi xử lý vision cơ bản (YOLOv8n-int8 + depth) trên thiết bị, không cần điện thoại.
- `PHONE`: Pi chỉ chụp frame, gửi lên điện thoại; điện thoại chạy model nặng, gửi kết quả lại.
- `AUTO` (mặc định):
  - Nếu điện thoại + Wi-Fi sẵn sàng → dùng `PHONE`.
  - Nếu mất kết nối/điện thoại không có → tự động chuyển về `LOCAL`.

**Quy tắc an toàn:**  
Bất kể mode nào, Pi luôn duy trì **tối thiểu** pipeline cảnh báo va chạm cơ bản (obstacle gần, vật thể lao tới) để đảm bảo an toàn ngay cả khi mất mạng / mất điện thoại.

## 4. Dòng dữ liệu (Data Flow) đơn giản

### 4.1. Pi – Phone (offload vision)

1. **Capture frame** (Pi – C++ `camera_service`).
2. Encode JPEG, gửi qua **WebSocket** tới user-app (nếu đang ở mode PHONE).
3. User-app nhận ảnh:
   - `VisionEngine` chạy YOLO, trả về danh sách object, vị trí, độ tin cậy.
4. User-app gửi lại `DetectionResult` cho Pi qua WebSocket.
5. Pi `fusion_engine` kết hợp:
   - detection + depth + ngữ cảnh (mặt người quen, vị trí).
6. `danger_analyzer` áp dụng `danger_rules.yaml`:
   - Nếu có nguy hiểm → tạo `DangerAlert`.
   - Gửi TTS và/hoặc notification lên app / cloud.

### 4.2. Pi – Cloud (offline-friendly)

- Khi có kết nối Internet (qua điện thoại hoặc Wi-Fi khác):
  - Pi hoặc user-app gửi **location**, **alerts** tới cloud.
- Khi mất mạng:
  - Events được ghi xuống log cục bộ.
  - Khi mạng trở lại, hệ thống gửi batch (tuỳ theo cấu hình, tránh spam).

## 5. Khởi động & tự vận hành

### 5.1. Trên Raspberry Pi Zero 2W

Flow:

1. Người dùng bật nguồn Pi (từ pin/battery pack).
2. RPi OS boot → systemd start:
   - `ai-glasses-core.service` (script `pi-core/scripts/run_all.sh`).
3. `run_all.sh`:
   - Khởi chạy `camera_service` (C++).
   - Khởi chạy `main.py` (orchestrator).
4. Orchestrator:
   - Đọc `system.yaml`, `power_profiles.yaml`.
   - Khởi tạo các service cần thiết.
   - Cố gắng kết nối WebSocket tới **điện thoại** (theo `network.yaml`).
   - Nếu không kết nối được:
     - Bật chế độ **offline**: chỉ chạy pipeline tối thiểu.

### 5.2. Trên điện thoại (User App)

Flow:

1. Điện thoại bật **hotspot** (SSID & mật khẩu đã cấu hình sẵn trong Pi).
2. Pi tự động kết nối vào hotspot (wpa_supplicant + network.yaml).
3. User-app:
   - Chạy background service `GlassesConnectionManager`.
   - Lắng nghe WebSocket trên port cố định (ví dụ 8765) hoặc connect tới Pi (tuỳ thiết kế).
   - Khi phát hiện Pi kết nối:
     - Thực hiện handshake (exchange device_id, version…).
     - Chuyển sang trạng thái **ONLINE–PHONE MODE**.

### 5.3. Chế độ offline an toàn

Nếu:

- Điện thoại tắt / mất kết nối.
- Mạng Wi-Fi/hotspot mất.
- Cloud không truy cập được.

→ Pi:

- Tự động chuyển về `LOCAL MODE`.
- Vẫn duy trì:
  - Cảnh báo vật cản, xe lao tới.
  - SOS button (gửi âm thanh cảnh báo cục bộ, ghi log).
- Khi mạng/điện thoại trở lại:
  - Orchestrator tự reconnect.
  - Trạng thái OFFLOAD lại được bật theo `AUTO`.

## 6. Ưu tiên tài nguyên & tiết kiệm pin

- Đặt FPS camera, độ phân giải, chu kỳ inference theo `power_profiles.yaml`.
- Chỉ bật các module cần thiết theo ngữ cảnh:
  - Navigation chỉ bật khi người dùng yêu cầu.
  - Face recognition chỉ bật trong mode tương ứng.
- Pi Zero 2W chỉ giữ các tác vụ nặng ở dạng **C++ tối ưu** + TFLite INT8.

---
