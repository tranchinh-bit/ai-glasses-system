# AI Glasses – User App (Android)

App dành cho **người đeo kính**, chạy trên Android.

Chức năng chính:

- Tự động **kết nối với kính (Pi)** qua WebSocket khi cùng mạng Wi-Fi / hotspot.
- Nhận **frame / event** từ Pi, xử lý offload (VisionEngine).
- Gửi **DetectionResult**, **ConfigUpdate**, **SOS**, v.v. về Pi.
- Cung cấp UI để:
  - Xem trạng thái kết nối.
  - Chọn chế độ offload (AUTO / LOCAL / PHONE).
  - Quản lý Places / Faces (khung sẵn, bạn có thể gắn backend sau).

Công nghệ:

- Kotlin + Jetpack Compose.
- OkHttp WebSocket (network).
- Kotlin Coroutines + Flow (state).
