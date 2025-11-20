# AI Glasses System

Hệ thống kính thông minh hỗ trợ người khiếm thị / mắt kém, gồm 3 phần chính:

- **Pi Core** – chạy trên Raspberry Pi Zero 2W, xử lý camera, nhận diện vật thể, phân tích nguy hiểm, quản lý nguồn.
- **Mobile Apps** – 2 app Android:
  - **User App**: dành cho người đeo kính (cài đặt, địa điểm quen, khuôn mặt quen, điều hướng…)
  - **Family App**: dành cho người thân (xem cảnh báo, xem vị trí, giám sát cơ bản)
- **Cloud Backend** – server FastAPI nhẹ, theo dõi vị trí & cảnh báo, cung cấp WebSocket cho Family App.

Ngoài ra có thư mục **shared/** chứa protocol (protobuf) và các file config YAML dùng chung cho tất cả.

---

## Cấu trúc repo

```text
ai-glasses-system/
├── README.md
├── Makefile
├── docs/                  # GĐ 1 – Tài liệu kiến trúc & thuật toán
├── shared/                # GĐ 2 – Thứ dùng chung (protocol, config)
│   ├── protocol/
│   │   ├── enums.proto
│   │   ├── messages.proto
│   │   └── gen/
│   │       ├── python/   # code sinh ra cho pi-core
│   │       └── java/     # code sinh ra cho mobile
│   ├── configs/
│   │   ├── power_profiles.yaml
│   │   ├── traffic_rules_vn.yaml
│   │   ├── danger_rules.yaml
│   │   └── tts_profiles.yaml
│   ├── api/
│   │   └── rest_openapi.yaml
│   └── tools/
│       └── generate_protos.sh
├── pi-core/               # GĐ 3 – Chạy trên Raspberry Pi Zero 2W
│   ├── README.md
│   ├── scripts/
│   ├── configs/
│   ├── models/
│   ├── data/
│   ├── src/
│   └── tests/
├── mobile/                # GĐ 4 – App điện thoại
│   ├── user-app/          # App người đeo kính
│   └── family-app/        # App người thân
├── cloud-backend/         # GĐ 5 – Server vị trí & cảnh báo
│   ├── README.md
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
└── tools/
    ├── dev-compose.yaml
    └── scripts/
        ├── build_all.sh
        └── check_style.sh
