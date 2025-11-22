
---

### `docs/06-deployment-and-ops.md`

```markdown
# 06 – Deployment and Ops

## 1. Mục tiêu

- Hướng dẫn triển khai hệ thống từ A–Z:
  - Raspberry Pi Zero 2W.
  - Mobile apps.
  - Cloud-backend.
- Đảm bảo:
  - **Bật nguồn là chạy** (Pi auto start, auto connect).
  - **Tự động kết nối** với điện thoại hotspot.
  - Có **chế độ offline an toàn**.
  - Có logging, monitoring cơ bản.

---

## 2. Triển khai trên Raspberry Pi Zero 2W

### 2.1. Chuẩn bị SD Card

1. Flash **Raspberry Pi OS Lite** (64-bit) lên thẻ microSD.
2. Cấu hình:
   - `wpa_supplicant.conf` với SSID/password của **hotspot điện thoại**.
   - File `ssh` để enable SSH (giai đoạn dev).

Ví dụ `wpa_supplicant.conf` (trên boot partition):

```conf
country=VN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="TEN_HOTSPOT_DIEN_THOAI"
    psk="MAT_KHAU_HOTSPOT"
    key_mgmt=WPA-PSK
}
