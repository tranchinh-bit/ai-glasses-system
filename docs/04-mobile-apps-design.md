
---

### `docs/04-mobile-apps-design.md`

```markdown
# 04 – Mobile Apps Design

## 1. Tổng quan

Có 2 app Android:

1. **User App** – dành cho người đeo kính.
2. **Family App** – dành cho người thân, caregiver.

Cả hai dùng chung protocol (Protobuf) và có thể dùng chung 1 số module (network, models) nếu tái sử dụng code.

---

## 2. User App (mobile/user-app)

### 2.1. Mục tiêu

- Tự động **kết nối với kính (Pi)** khi chung Wi-Fi/hotspot.
- Nhận frame từ Pi, chạy YOLO nặng hơn (FP16/GPU).
- Xử lý:
  - Vision.
  - Navigation.
  - Voice (TTS/ASR nếu cần).
- Cung cấp UI cho người dùng (hoặc người hỗ trợ) để:
  - Cấu hình profile.
  - Quản lý faces, places.
  - Xem logs cơ bản.

### 2.2. Kiến trúc code

Thư mục chính:

- `java/com/ai_glasses/userapp/`
  - `UserApp.kt`: Application class.
  - `MainActivity.kt`: entry UI, điều hướng màn hình.
  - `GlassesConnectionManager.kt`: quản lý WebSocket Pi ↔ App.
  - `VisionEngine.kt`: chạy model YOLO trên phone.
  - `VoiceService.kt`: TTS, ASR (nếu có).
  - `NavigationService.kt`: sử dụng Google Maps API hoặc OSRM.
  - `data/`
    - `UserPreferences.kt`: Lưu config (mode, profile…).
    - `PlacesRepository.kt`: Lưu familiar places.
  - `ui/`
    - `HomeScreen.kt`
    - `PlacesScreen.kt`
    - `FacesScreen.kt`
    - `SettingsScreen.kt`

### 2.3. Flow kết nối tự động

1. Khi app khởi động:
   - `UserApp.onCreate()`:
     - Khởi tạo `GlassesConnectionManager` dưới dạng singleton.
2. `GlassesConnectionManager`:
   - Đọc config địa chỉ Pi (từ `UserPreferences` hoặc auto-discovery).
   - Thử connect WebSocket (AUTO reconnect).
   - Khi kết nối thành công:
     - Dispatch event “Kính đã online” cho UI.
3. Nếu Wi-Fi thay đổi, hotspot bật/tắt:
   - Lắng nghe broadcast của hệ thống.
   - Thử reconnect tới Pi.

### 2.4. Flow offload vision

1. Nhận `VisionFrame` từ Pi.
2. `VisionEngine`:
   - Chạy YOLO (TensorRT/NNAPI nếu có).
   - Trả về `DetectionResult`.
3. `GlassesConnectionManager` gửi `DetectionResult` lại cho Pi.
4. Nếu cần, app cũng có thể tự phát TTS (VD: khi Pi muốn offload TTS).

### 2.5. UI & Màn hình

- **HomeScreen:**
  - Trạng thái kết nối kính.
  - Nút nhanh: “Bật/tắt offload”, “SOS”, “Chọn profile pin”.
- **PlacesScreen:**
  - Danh sách familiar places.
  - Thêm/sửa/xoá.
  - Gửi `NavCommand` cho Pi khi chọn “Đi tới …”.
- **FacesScreen:**
  - Danh sách người quen.
  - Chụp/gửi ảnh lên Pi để enroll faces.
- **SettingsScreen:**
  - Cấu hình `offload_mode`, ngôn ngữ, TTS profile.
  - Tắt/bật cloud-backend.

---

## 3. Family App (mobile/family-app)

### 3.1. Mục tiêu

- Theo dõi vị trí kính theo thời gian thực.
- Nhận thông báo SOS, Danger Alert từ cloud.
- Không cần thiết phải ở cùng mạng với Pi.

### 3.2. Kiến trúc

Thư mục chính:

- `java/com/ai_glasses/familyapp/`
  - `MainActivity.kt`
  - `BackendClient.kt`: kết nối REST + WebSocket tới cloud.
  - `data/`
    - `DeviceSelectionRepository.kt`
    - `AlertsRepository.kt`
  - `ui/`
    - `MapScreen.kt`: hiển thị vị trí hiện tại / history.
    - `AlertsScreen.kt`: danh sách cảnh báo, SOS.
    - `SettingsScreen.kt`: chọn kính, cấu hình thông báo.

### 3.3. Flow hoạt động

1. User đăng nhập/chọn thiết bị (device_id).
2. `BackendClient` mở WebSocket tới `wss://cloud/ws/family?device_id=...`.
3. Khi có `DangerAlert`, `SOS`, `HealthStatus`:
   - Hiển thị notification local.
   - Cập nhật UI map/alerts.

---

## 4. Thiết kế trải nghiệm offline

### 4.1. User App

- Nếu app không kết nối được Pi:
  - Hiển thị trạng thái “Kính offline”.
  - Cho phép xem lại logs cũ, cấu hình offline.
- Nếu không có Internet:
  - Vẫn có thể giao tiếp với Pi qua Wi-Fi/hotspot.
  - Không gửi được dữ liệu lên cloud → buffer bởi app (tùy config).

### 4.2. Family App

- Nếu mất kết nối cloud:
  - Hiển thị trạng thái “Server offline / không có mạng”.
  - Chỉ xem được lịch sử data đã cache (nếu có).

---

## 5. Quy tắc an toàn & ưu tiên

- User App không bao giờ được chặn hoặc làm chậm pipeline an toàn trên Pi:
  - Nếu app không kịp xử lý frame → Pi phải có timeout và xử lý local.
- App không được tự ý chuyển Pi sang mode nguy hiểm (tắt hoàn toàn vision).
- Khi user nhấn SOS:
  - Ưu tiên tuyệt đối gửi thông báo tới family/cloud nếu có mạng.
  - Nếu không, vẫn phải feedback lại cho người đeo (âm thanh/voice).

---
