# 05 – Cloud Backend Design

## 1. Mục tiêu

- Lưu trữ & cung cấp:
  - **Vị trí** của kính.
  - **Cảnh báo nguy hiểm**, **SOS**.
  - **Health status** (CPU, pin, nhiệt độ…).
- Cung cấp WebSocket realtime cho Family App.
- Triển khai được trên server nhỏ / VPS / thậm chí Raspberry Pi khác.

## 2. Tech stack

- **FastAPI** (Python).
- **Uvicorn** (ASGI server).
- **SQLite** (dev) / **Postgres** (prod).
- **SQLAlchemy** (ORM).
- **Pydantic** (schemas).
- **WebSocket** cho realtime update.

Thư mục:

- `cloud-backend/app/main.py`
- `cloud-backend/app/models.py`
- `cloud-backend/app/schemas.py`
- `cloud-backend/app/routers/`
- `cloud-backend/app/ws/family_ws.py`

## 3. API endpoints

### 3.1. Location

- `POST /api/v1/location/update`
  - Body:
    - `device_id`, `lat`, `lon`, `accuracy`, `timestamp`.
- `GET /api/v1/location/latest?device_id=...`
  - Trả về location mới nhất.

### 3.2. Alerts

- `POST /api/v1/alerts`
  - Body:
    - `device_id`, `level`, `message`, `rule_id`, `timestamp`.
- `GET /api/v1/alerts?device_id=...&since=...`
  - Lấy danh sách alert mới.

### 3.3. Health

- `POST /api/v1/health`
  - Body:
    - `device_id`, `cpu_usage`, `mem_usage`, `temperature_c`, `battery_percent`, `offload_mode`.
- `GET /api/v1/health/latest?device_id=...`

### 3.4. Health check

- `GET /health`
  - Kiểm tra server sống.

## 4. WebSocket – Family channel

- Endpoint: `GET /ws/family`
  - Query params:
    - `device_id`.
- Khi client (family-app) kết nối:
  - Đăng ký device_id quan tâm.
  - Server giữ connection trong pool.

Khi có sự kiện:

- `LocationUpdate` mới.
- `DangerAlert` mới (từ Pi/phone).
- `SOS` event.
- `HealthStatus` critical.

→ Backend push message qua WS cho các client subscribe.

Message format: JSON đơn giản:

```json
{
  "type": "alert",
  "device_id": "glasses-001",
  "payload": {
    "level": "CRITICAL",
    "message": "Xe đang lao tới phía trước, hãy dừng lại!",
    "timestamp": 1697044378000
  }
}
