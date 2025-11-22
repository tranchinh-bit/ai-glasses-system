# AI Glasses – Pi Core (Raspberry Pi Zero 2W)

Đây là phần “core” chạy trên **Raspberry Pi Zero 2W** gắn trên kính.

Nhiệm vụ:

- Điều khiển pipeline camera + vision (YOLO, depth).
- Giao tiếp với điện thoại (User App) qua WebSocket.
- Chuyển mode OFFLOAD:
  - `AUTO` – ưu tiên offload lên phone, fallback LOCAL.
  - `LOCAL` – xử lý trên Pi.
  - `PHONE` – chỉ offload, không chạy YOLO local.
- Duy trì **safety pipeline tối thiểu** ngay cả khi:
  - Mất điện thoại.
  - Mất Internet.
- Gửi heartbeat, health, alerts lên điện thoại / cloud.

Cách chạy:

```bash
cd pi-core
./scripts/install_pi.sh     # lần đầu trên Pi
./scripts/run_all.sh        # chạy thử tay
./scripts/setup_systemd.sh  # cài systemd để bật nguồn là auto chạy
