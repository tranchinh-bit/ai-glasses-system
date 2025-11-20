# 01 – Protocol and Messages

This document defines the **logical protocol** between:

- Glasses (Raspberry Pi Zero 2 W)
- User App (phone of the user)
- Family App (phone of family/caregiver)
- Backend (optional cloud service)

The actual serialized format in `shared/` will be **Protobuf** for maximum speed and low bandwidth.  
Here we define the **semantics, fields, and message flows** in a transport-agnostic way.

---

## 1. Transport Layers

### 1.1. Glasses ↔ User App

- **Medium:** Wi-Fi (phone hotspot or shared Wi-Fi).
- **Transport:** WebSocket over TCP.
- **Direction:**
  - Glasses runs a **WebSocket server** on configurable port (default `:9000`).
  - User App connects as **client**.
- **Connection model:**
  - 1 persistent connection per glasses ↔ phone pair.
  - Auto-reconnect with exponential backoff on the User App side.

> Nguyên tắc: kính luôn cố gắng đơn giản, mọi logic phức tạp (reconnect, retry) để điện thoại làm.

---

### 1.2. User App ↔ Backend

- **Transport:**
  - HTTPS REST (for CRUD / history / config sync).
  - WebSocket (or SSE) for realtime events (location updates, alerts, status).
- **Responsibility:**
  - User App acts as a **gateway**:
    - Receives messages from Glasses.
    - Forwards relevant items (SOS, location, status) to Backend.
    - Receives updates/routes/commands from Backend when needed.

---

### 1.3. Family App ↔ Backend

- **Transport:** WebSocket for realtime updates.
- **Responsibility:**
  - Subscribe to:
    - Location stream.
    - SOS alerts.
    - Device health alerts (optional).
  - No direct connection to Glasses; everything goes through Backend.

---

## 2. Common Envelope

All messages passing between devices/apps/backend **share a common envelope**.

```jsonc
{
  "type": "status_update",        // logical message type
  "protocol_version": 1,
  "msg_id": "uuid-or-incr",
  "timestamp": 1710000000,        // unix seconds
  "device_id": "glasses_001",     // or phone_xxx / backend
  "user_id": "user_01",           // optional on some links
  "payload": { /* type-specific */ }
}
{
  "type": "status_update",
  "protocol_version": 1,
  "msg_id": "st_123",
  "timestamp": 1710000000,
  "device_id": "glasses_001",
  "payload": {
    "battery_pct": 72,
    "cpu_temp_c": 48.5,
    "cpu_load_pct": 63,
    "mode": "navigation",          // navigation, ocr, money, face, idle
    "power_profile": "balanced",   // super_save, balanced, performance
    "wifi_rssi": -58,
    "uptime_s": 3600,
    "is_online_with_backend": true // whether phone ↔ backend link is healthy
  }
}
{
  "type": "alert",
  "protocol_version": 1,
  "msg_id": "al_001",
  "timestamp": 1710000000,
  "device_id": "glasses_001",
  "payload": {
    "subtype": "sos",          // sos, health_issue, camera_error, wifi_lost, battery_low, ...
    "severity": "high",        // info, warning, high, critical
    "source": "user",          // user, system, vision, health_monitor
    "location": {
      "lat": 10.1234,
      "lon": 106.9876,
      "accuracy_m": 20.0
    },
    "message": "User pressed SOS button",
    "extra": {
      "cpu_temp_c": 70.2,
      "battery_pct": 18
    }
  }
}
{
  "type": "voice_request",
  "protocol_version": 1,
  "msg_id": "vr_123",
  "timestamp": 1710000000,
  "device_id": "glasses_001",
  "payload": {
    "request_id": "vr_123",      // used to match reply
    "audio_format": "pcm16",     // pcm16, opus, ...
    "sample_rate": 16000,
    "language": "vi-VN",
    "chunk_index": 0,            // 0..N-1 for streaming
    "chunk_count": 1,            // total number of chunks
    "is_final_chunk": true,
    "data": "<base64-encoded-audio>"
  }
}
{
  "type": "context_snapshot",
  "protocol_version": 1,
  "msg_id": "cs_001",
  "timestamp": 1710000000,
  "device_id": "glasses_001",
  "payload": {
    "location": { "lat": 10.1234, "lon": 106.9876, "accuracy_m": 10.0 },
    "mode": "navigation",
    "objects": [
      { "class": "person", "distance_m": 2.5, "direction": "front" },
      { "class": "motorbike", "distance_m": 4.0, "direction": "right" }
    ],
    "traffic_context": {
      "density": "medium",          // low, medium, high
      "has_crosswalk": true,
      "has_traffic_light": false,
      "road_type": "urban_street"   // optional enum
    }
  }
}
{
  "type": "voice_reply",
  "protocol_version": 1,
  "msg_id": "vrp_123",
  "timestamp": 1710000002,
  "device_id": "glasses_001",
  "payload": {
    "request_id": "vr_123",
    "text": "Phía trước có hai người đi bộ và một xe máy bên phải.",
    "priority": "normal",     // low, normal, high
    "voice_profile": "default_female", // optional
    "can_interrupt_lower_priority": true
  }
}
{
  "type": "navigation_step",
  "protocol_version": 1,
  "msg_id": "nav_005",
  "timestamp": 1710000100,
  "device_id": "glasses_001",
  "payload": {
    "route_id": "route_20250301_01",
    "step_id": 5,
    "is_final": false,
    "distance_m": 40.0,
    "direction": "left",                // left, right, straight, uturn
    "street_name": "Nguyễn Văn Thoại",
    "spoken_hint": "Bốn mươi mét nữa rẽ trái vào đường Nguyễn Văn Thoại.",
    "eta_s": 25                         // optional
  }
}
{
  "type": "config_update",
  "protocol_version": 1,
  "msg_id": "cfg_001",
  "timestamp": 1710000200,
  "device_id": "glasses_001",
  "payload": {
    "tts_speed": "slow",              // slow, normal, fast
    "talk_level": "short",            // short, normal, verbose
    "power_profile": "super_save",    // super_save, balanced, performance
    "features": {
      "face_recognition": true,
      "ocr": true,
      "traffic_context": true
    },
    "language": "vi-VN",
    "night_mode_enabled": true
  }
}
{
  "type": "place_update",
  "protocol_version": 1,
  "msg_id": "pl_001",
  "timestamp": 1710000300,
  "device_id": "glasses_001",
  "payload": {
    "action": "save",                      // save, delete
    "name": "home",
    "location": { "lat": 10.1234, "lon": 106.9876, "accuracy_m": 12.0 },
    "note": "cổng nhà chính"
  }
}
{
  "type": "command",
  "protocol_version": 1,
  "msg_id": "cmd_001",
  "timestamp": 1710000400,
  "device_id": "glasses_001",
  "payload": {
    "command": "switch_mode",            // switch_mode, repeat_last, mute, unmute, sos_ack, ping, ...
    "args": {
      "mode": "ocr"
    }
  }
}
{
  "type": "location_update",
  "protocol_version": 1,
  "msg_id": "loc_001",
  "timestamp": 1710000500,
  "user_id": "user_01",
  "device_id": "glasses_001",
  "payload": {
    "lat": 10.1234,
    "lon": 106.9876,
    "accuracy_m": 15,
    "source": "phone_gps"         // phone_gps, glasses_gps, manual
  }
}
{
  "type": "alert_forward",
  "protocol_version": 1,
  "msg_id": "al_fwd_001",
  "timestamp": 1710000505,
  "user_id": "user_01",
  "device_id": "glasses_001",
  "payload": {
    "type": "sos",
    "severity": "high",
    "message": "SOS: User pressed emergency button.",
    "location": { "lat": 10.1234, "lon": 106.9876, "accuracy_m": 20.0 },
    "raw_alert_id": "al_001"
  }
}
