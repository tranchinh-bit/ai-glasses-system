# AI Glasses Cloud Backend

Backend nhẹ cho hệ thống Kính Thông Minh.

### Nhiệm vụ

- Nhận & lưu **location update** từ kính / điện thoại.
- Nhận & lưu **alerts** (SOS, danger alerts).
- Đẩy realtime **alert + location** tới **Family App** qua WebSocket.
- Cung cấp API health check để Pi / App kiểm tra.

### Tech stack

- FastAPI
- SQLite (SQLAlchemy)
- Uvicorn
- WebSocket (FastAPI / Starlette)

---

## Cấu trúc thư mục

```text
cloud-backend/
├── README.md
├── requirements.txt
├── Dockerfile
├── alembic/              # (tuỳ chọn – nếu dùng Postgres/migration)
│   └── ...
└── app/
    ├── main.py
    ├── config.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── deps.py
    ├── routers/
    │   ├── locations.py
    │   ├── alerts.py
    │   └── health.py
    └── ws/
        └── family_ws.py
