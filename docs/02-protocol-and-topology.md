# 02 – Protocol and Network Topology

## 1. Mục tiêu

- Đảm bảo **Pi–Phone** giao tiếp ổn định, tiết kiệm băng thông, không phụ thuộc Internet.
- Cho phép **offload** vision / navigation / voice lên điện thoại.
- Hỗ trợ **cloud-backend** để người thân theo dõi từ xa.
- Hỗ trợ **offline mode**: khi không có Internet vẫn an toàn.

## 2. Topology mạng

### 2.1. Chế độ thông thường (Phone hotspot)

- Điện thoại tạo **Wi-Fi hotspot**:
  - SSID: do người dùng cấu hình.
  - Mật khẩu: được lưu trong `wpa_supplicant.conf` và `pi-core/configs/network.yaml`.
- Raspberry Pi Zero 2W:
  - Kết nối vào hotspot như 1 **Wi-Fi client**.
- User App:
  - Lắng nghe hoặc kết nối WebSocket với Pi trong cùng subnet.

Ví dụ:

- Hotspot phone: `192.168.43.1`
- Pi Zero 2W (DHCP): `192.168.43.10`
- Pi → User-app: `ws://192.168.43.1:8765`  
  hoặc
- User-app → Pi: `ws://192.168.43.10:9000`

(Tuỳ cách triển khai, nhưng repo hiện tại assume Pi **client** gọi lên app.)

### 2.2. Chế độ tại nhà (Home/Office Wi-Fi)

- Pi kết nối vào Wi-Fi nhà (SSID + password đã được provisioning).
- Điện thoại cũng kết nối cùng Wi-Fi.
- Giao tiếp Pi ↔ phone vẫn qua WebSocket, nhưng IP sẽ do router cấp.

### 2.3. Kết nối lên Cloud

Hai đường:

1. **Pi → Cloud**: gửi health, alerts, location (nếu cấu hình).
2. **User App → Cloud**: cũng có thể gửi events thay Pi, tuỳ phần thiết kế.

Family-app:

- Kết nối tới cloud-backend qua HTTPS + WebSocket.
- Nhận dữ liệu từ `ws/family_ws.py`.

## 3. Port & dịch vụ

Đề xuất port (có thể chỉnh trong config):

- **Pi Core:**
  - IPC camera → Python: UNIX socket hoặc TCP local (e.g. 127.0.0.1:5555).
  - Metrics (optional): HTTP `localhost:9100` (Prometheus/exporter).
- **Pi ↔ Phone:**
  - WebSocket: `ws://PHONE_IP:8765/api/v1/glasses` (User app mở server).
- **Phone ↔ Cloud:**
  - HTTP REST: `https://api.aiglasses.cloud/api/v1/...`
  - WebSocket: `wss://api.aiglasses.cloud/ws/family` (Family app).

## 4. Protocol – Protobuf messages

Các file `.proto`:

- `shared/protocol/enums.proto`
- `shared/protocol/messages.proto`

### 4.1. Các enum chính (gợi ý)

```proto
enum OffloadMode {
  OFFLOAD_AUTO = 0;
  OFFLOAD_LOCAL = 1;
  OFFLOAD_PHONE = 2;
}

enum EventType {
  EVENT_UNKNOWN = 0;
  EVENT_DANGER_ALERT = 1;
  EVENT_SOS = 2;
  EVENT_HEARTBEAT = 3;
  EVENT_NAVIGATION_UPDATE = 4;
}

enum DangerLevel {
  DANGER_NONE = 0;
  DANGER_LOW = 1;
  DANGER_MEDIUM = 2;
  DANGER_HIGH = 3;
  DANGER_CRITICAL = 4;
}
message VisionFrame {
  string device_id = 1;
  int64 timestamp_ms = 2;
  bytes jpeg_data = 3;
  int32 width = 4;
  int32 height = 5;
  // Optional: compressed depth map, etc.
}
message DetectionResult {
  string device_id = 1;
  int64 timestamp_ms = 2;
  repeated DetectionItem items = 3;
}

message DetectionItem {
  int32 class_id = 1;
  string label = 2;
  float confidence = 3;
  float x_center = 4;
  float y_center = 5;
  float width = 6;
  float height = 7;
  // Optional: estimated distance, angle.
}
message DangerAlert {
  string device_id = 1;
  int64 timestamp_ms = 2;
  DangerLevel level = 3;
  string message_tts = 4;
  string rule_id = 5;
}
message HealthStatus {
  string device_id = 1;
  int64 timestamp_ms = 2;
  float cpu_usage = 3;
  float mem_usage = 4;
  float temperature_c = 5;
  float battery_percent = 6;
  OffloadMode current_mode = 7;
}
message NavCommand {
  string device_id = 1;
  string target_place_id = 2;
  double target_lat = 3;
  double target_lon = 4;
}

message NavUpdate {
  string device_id = 1;
  double current_lat = 2;
  double current_lon = 3;
  string instruction_tts = 4;
}
message VoiceCommand {
  string device_id = 1;
  int64 timestamp_ms = 2;
  string text = 3;  // ASR result
}
message WsEnvelope {
  string msg_id = 1;
  string device_id = 2;
  int64 timestamp_ms = 3;
  oneof payload {
    VisionFrame vision_frame = 10;
    DetectionResult detection_result = 11;
    DangerAlert danger_alert = 12;
    HealthStatus health_status = 13;
    NavCommand nav_command = 14;
    NavUpdate nav_update = 15;
    VoiceCommand voice_command = 16;
  }
}
