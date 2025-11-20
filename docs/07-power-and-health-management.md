# 07 – Power & Health Management

## 1. Power Profiles

### 1.1. super_save

- Camera:
  - OFF or 1 FPS.
- Vision services:
  - All OFF by default.
- Audio:
  - Wake word listener ON (low-cost).
- Networking:
  - Minimal: only maintain connection if available.
- Use case:
  - User sitting or resting, no walking.

### 1.2. balanced

- Camera:
  - ON at moderate FPS (8–10).
- Vision:
  - `vision_object_danger` ON with moderate FPS (4–6).
  - Others OFF unless explicitly enabled by user.
- Use case:
  - Normal walking, default everyday mode.

### 1.3. performance

- Camera:
  - ON at highest reasonable FPS (e.g., 15).
- Vision:
  - `vision_object_danger` at max stable FPS.
  - Temporary enabling of multiple modules allowed.
- Use case:
  - High-risk environments or testing.

---

## 2. Power Manager

Responsible for:

- Switching profiles.
- Enforcing:
  - Which services are running.
  - Camera FPS and vision inference frequency.

Inputs:

- User/App configuration (from User App).
- Battery level.
- Health monitor data (temperature, CPU load).

Behavior:

- When battery is low:
  - Force `super_save` or `balanced`.
- When temperature is high:
  - Reduce FPS & disable non-critical vision modules.

---

## 3. Health Monitor

Checks periodically:

- CPU temperature.
- CPU utilization.
- Free RAM.
- Camera status:
  - Can frames still be captured?
- Wi-Fi connection status.

Outputs:

- `HealthAlert` events to `core_orchestrator` and `io_hub`.

User-facing behavior:

- Example phrases:
  - “Kính đang nóng, hãy nghỉ sử dụng một lúc.”
  - “Pin còn thấp, hãy sạc kính sớm.”
  - “Mất kết nối với điện thoại, chuyển sang chế độ offline.”

Family-facing behavior:

- For severe cases:
  - Alerts sent to backend, then to Family App.

---

## 4. Implementation Strategy

- Use OS utilities or direct reads:
  - `/sys/class/thermal/...` for temperature.
  - `/proc/stat` for CPU usage.
  - `/proc/meminfo` for RAM.
- Health checks should be lightweight and run at low frequency (e.g., every 5–10 s).
