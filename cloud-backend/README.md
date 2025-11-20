# AI Glasses Cloud Backend

Backend nhẹ cho hệ thống AI Glasses:

- Lưu vị trí hiện tại của thiết bị (kính / điện thoại)
- Lưu lịch sử cảnh báo (hazard, SOS...)
- Cung cấp REST API cho mobile app
- Cung cấp WebSocket `/ws/family` cho Family App nhận realtime alert

## Tech stack

- Python 3.11+
- FastAPI
- SQLite (SQLAlchemy async)
- WebSocket

## Cài đặt & chạy (dev)

```bash
cd cloud-backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
