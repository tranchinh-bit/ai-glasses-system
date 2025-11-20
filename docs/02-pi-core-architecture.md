
---

## `docs/02-pi-core-architecture.md`

```markdown
# 02 – Pi Core Architecture (Glasses Runtime)

This document describes the **runtime architecture** of the smart glasses running on **Raspberry Pi Zero 2 W**.

Goals:

- Run efficiently on constrained hardware.
- Prioritize **low-latency danger detection**.
- Provide **smooth audio feedback**.
- Offload heavy cloud tasks (STT/LLM/maps) to smartphones.
- Maintain a **modular, resilient** design.

---

## 1. Process Overview

All major functionality is split into **separate services/processes**.  
Each service has a well-defined responsibility and communicates via an internal **event bus**.

### 1.1. List of Core Processes

1. `core_orchestrator` (Python)
2. `camera_service` (C++ / Python)
3. `vision_object_danger` (C++)
4. `vision_ocr_currency` (C++ + Python)
5. `vision_face` (C++ + Python)
6. `fusion_engine` (Python)
7. `voice_dialog_client` (Python)
8. `navigation_client` (Python)
9. `io_hub` (Python)
10. `ir_input` (Python/C++)
11. `power_manager` (Python)
12. `health_monitor` (Python)

Optionally, a **supervisor** (e.g. `systemd` or a lightweight Python supervisor) can restart individual services when they crash.

---

## 2. Service Responsibilities

### 2.1. `core_orchestrator` (Python)

**Role:** Central brain of the glasses.

- Tracks:
  - Current **mode**: `navigation`, `ocr`, `money`, `face`, `idle`.
  - Current **power profile**: `super_save`, `balanced`, `performance`.
- Subscribes to events from:
  - `fusion_engine` (vision & context).
  - `voice_dialog_client` (voice requests/replies).
  - `navigation_client` (navigation steps).
  - `ir_input` (remote control).
  - `health_monitor` (alerts).
  - `io_hub` (commands/config from User App).
- Decisions:
  - When to speak which message (danger alerts override other TTS).
  - When to switch modes.
  - When to change power profile (e.g., low battery → `super_save`).
- Interfaces:
  - Sends TTS text to `voice_dialog_client`.
  - Sends minimal status + high-level events to `io_hub` for User App/Backend.
  - Instructs `power_manager` to enable/disable services.

---

### 2.2. `camera_service` (C++ / Python)

**Role:** Sole owner of camera hardware.

- Captures frames at configurable resolution/FPS, e.g.:
  - `640×480 @ 15 FPS` (navigation).
  - Lower FPS for power saving.
- Writes frames into a **shared memory ring buffer**:
  - Vision services always read **latest frame only** to avoid backlog.
- Ensures:
  - Stable camera configuration (exposure, gain).
  - Graceful handling when camera errors occur (notify `health_monitor`).

---

### 2.3. `vision_object_danger` (C++)

**Role:** Primary **real-time perception** service.

- Reads frames from shared buffer.
- Performs:
  - Object detection (TFLite YOLO).
  - Tracking (e.g. SORT / IoU-based).
  - Distance estimation (mono depth heuristics or ToF integration).
  - Relative motion analysis → detect approaching objects.
  - Traffic context estimation:
    - density: `low`, `medium`, `high`.
    - presence of crosswalk or traffic light if models allow.
- Outputs:
  - `VisionObjectUpdate` events.
  - `DangerEvent` events.
  - `TrafficContextUpdate` events.

This service is usually **always on** (or at reduced FPS) in `navigation` mode.

---

### 2.4. `vision_ocr_currency` (C++ + Python)

**Role:** OCR (reading text) & currency recognition.

- Runs only in specific modes:
  - `ocr` mode:
    - Text detection (e.g. DB/CRAFT).
    - Text recognition (Vietnamese, English).
    - Aggregates text into reading order and sends `OcrResult`.
  - `money` mode:
    - Specialized classifier for Vietnamese banknotes.
    - Optionally uses attention on central region of frame.
- Controlled by:
  - `core_orchestrator` via events / config.
- Disabled in `navigation` mode to save CPU, unless explicitly requested.

---

### 2.5. `vision_face` (C++ + Python)

**Role:** Face detection and recognition.

- Responsibilities:
  - Detect faces in frame.
  - Compute embeddings.
  - Compare against enrolled faces.
  - Emit:
    - `FaceRecognized` events.
    - `FaceEnrollmentNeeded` (if user requested to save new face).
- Modes:
  - Active primarily in `face` mode.
  - Optionally low-FPS/background in other modes if allowed by power profile.

---

### 2.6. `fusion_engine` (Python)

**Role:** Combine all perception signals into coherent events.

- Inputs:
  - `VisionObjectUpdate`
  - `DangerEvent`
  - `TrafficContextUpdate`
  - `OcrResult`
  - `CurrencyResult`
  - `FaceRecognized`
  - Navigation hints (`NavStepArrived`)
- Tasks:
  - Assign priorities (danger > nav > info).
  - Deduplicate similar messages.
  - Rate-limit identical or low-value events.
  - Build **compact text summaries** such as:
    - “Trước mặt hai mét có xe máy đang chạy tới.”
    - “Đã thấy vạch qua đường phía trước.”
- Outputs:
  - `SummarizedEvent` for `core_orchestrator`.

---

### 2.7. `voice_dialog_client` (Python)

**Role:** Manage microphone input and TTS playback.

- Microphone:
  - Activates on wake word or IR button.
  - Records audio, splits into chunks.
  - Sends `voice_request` messages via `io_hub` to User App.
- TTS:
  - Receives `voice_reply` text from `io_hub`/`core_orchestrator`.
  - Queues messages with priority:
    - High priority: danger alerts.
    - Normal: navigation instructions.
    - Low: informational responses.
  - Handles:
    - Interrupting low-priority playback when a high-priority message arrives.
    - Optional beep/earcon for SOS, mode change.

---

### 2.8. `navigation_client` (Python)

**Role:** Receive and manage navigation steps.

- Inputs:
  - `navigation_step` messages from User App (via `io_hub`).
- Tasks:
  - Cache current route (`route_id` + steps).
  - Track progress (e.g., step index).
  - Notify `core_orchestrator` when:
    - A new step becomes relevant.
    - The route is finished.
- Integrates with:
  - `fusion_engine` to avoid conflicting speech with danger alerts.

---

### 2.9. `io_hub` (Python)

**Role:** Networking hub between Glasses and User App.

- Functions:
  - Maintains WebSocket connection to User App.
  - Serializes/deserializes messages using shared Protobuf.
  - Performs basic validation (`protocol_version`, required fields).
  - Routes incoming messages to correct internal components through event bus.
- Incoming examples:
  - `voice_reply` → `voice_dialog_client`
  - `navigation_step` → `navigation_client`
  - `config_update` → `core_orchestrator`
  - `command` → `core_orchestrator`
- Outgoing examples:
  - `status_update` → User App / Backend
  - `alert` → User App / Backend
  - `voice_request` → User App
  - `context_snapshot` → User App

---

### 2.10. `ir_input` (Python/C++)

**Role:** Remote control handling (e.g., HX1838 IR receiver).

- Tasks:
  - Read IR signals and decode remote control codes.
  - Map codes to internal events:
    - `IrButtonPressed` with `button_id` (`sos`, `mode_nav`, `mode_ocr`, `volume_up`, etc.).
  - De-bounce repeated signals.
- User experience:
  - Provides non-voice control for visually impaired users.

---

### 2.11. `power_manager` (Python)

**Role:** Manage energy usage to extend battery life.

- Power profiles:
  - `super_save`:
    - Reduced camera FPS.
    - Minimal vision services.
    - Very limited background tasks.
  - `balanced`:
    - Default usage profile.
  - `performance`:
    - Maximum FPS and active modules (short term).
- Controls:
  - Camera resolution & FPS (via `camera_service`).
  - Activation state of `vision_*` services.
  - CPU governor / frequency scaling (where supported).
- Triggered by:
  - `core_orchestrator` (via config or user preference).
  - `health_monitor` (e.g., high temperature, low battery).

---

### 2.12. `health_monitor` (Python)

**Role:** Monitor system health and send alerts.

- Periodic checks:
  - CPU temperature.
  - CPU load.
  - RAM usage.
  - Disk usage.
  - Camera availability.
  - Wi-Fi connectivity.
- Actions:
  - Emit `HealthAlert` events on thresholds.
  - If conditions are critical:
    - Instruct `core_orchestrator` to warn the user.
    - Instruct `power_manager` to downgrade profile.
    - Send alerts via `io_hub` to User App.

---

## 3. Internal Communication

### 3.1. Event Bus Design

Implementation options:

- ZeroMQ PUB/SUB sockets.
- Python `asyncio` event router using Unix domain sockets.
- Any lightweight message bus that:
  - Supports multiple publishers and subscribers.
  - Is low-latency and low-overhead.

Core event types:

- `VisionObjectUpdate`
- `DangerEvent`
- `TrafficContextUpdate`
- `OcrResult`
- `CurrencyResult`
- `FaceRecognized`
- `NavStepArrived`
- `VoiceRequestStarted`
- `VoiceReplyReady`
- `IrButtonPressed`
- `HealthAlert`
- `SummarizedEvent`
- `ConfigChanged`
- `PowerProfileChanged`

All events should include:

- `timestamp`
- `source_service`
- `type` (event type)
- `payload` (event-specific data)

---

## 4. Modes & Control Logic

### 4.1. Modes

The system operates in one of several modes:

1. `navigation`
   - `vision_object_danger`: full speed.
   - `vision_ocr_currency` & `vision_face`: disabled by default.
   - Basic forward obstacle detection always ON.

2. `ocr`
   - `vision_ocr_currency` (OCR pipeline): enabled.
   - `vision_object_danger`: reduced FPS or downgraded (basic obstacle detection only).
   - Used when user explicitly requests to read signs, labels, documents.

3. `money`
   - `vision_ocr_currency` in currency mode: enabled.
   - Other heavy services paused except minimal danger detection.

4. `face`
   - `vision_face`: enabled at low FPS (configurable).
   - `vision_object_danger`: may run at reduced FPS for safety.

5. `idle`
   - All heavy vision services disabled.
   - Keeps:
     - `ir_input`
     - `voice_dialog_client` (for wake word/button)
     - `health_monitor`
     - `io_hub` (connection to phone)

---

### 4.2. Mode Transitions

Triggers:

- IR remote:
  - Buttons for `navigation`, `ocr`, `money`, `face`, `idle`.
  - SOS button → `alert`.
- Voice commands:
  - “đi tới …”, “đọc giúp tôi”, “xem tiền”, “xem ai trước mặt” → mapped via User App.
- App configuration:
  - `config_update` messages from User App.

Rules (enforced by `core_orchestrator`):

- At most **one heavy vision service** active at a time (except short overlap when switching).
- Safety:
  - A minimal forward obstacle detection layer can remain active in non-navigation modes.
- Power profile coordination:
  - Some modes may force a minimum profile:
    - e.g. `navigation` might require at least `balanced`.

---

## 5. Audio Path & TTS

### 5.1. TTS Sources

- On-device TTS:
  - Lightweight offline voice engine.
  - Guaranteed latency (no network required).
- Remote TTS (optional future):
  - Voice generated on phone/cloud then sent as audio.

In current baseline design, the glasses play **TTS locally** and receive only **text** from the User App.

---

### 5.2. Priority & Interruption Rules

- Message categories:
  - **High priority**: danger alerts (`DangerEvent`).
  - **Medium priority**: navigation instructions.
  - **Low priority**: general information, chat replies.
- `voice_dialog_client`:
  - Interrupts lower priority audio if a higher priority message arrives.
  - Optionally plays short earcons (beeps) before high priority alerts.

---

## 6. Error Handling & Recovery

### 6.1. Service Supervision

- Each service:
  - Should be independently restartable.
  - Should register heartbeat with `health_monitor`.
- If a service fails:
  - Supervisor (systemd or custom) restarts it.
  - `health_monitor` issues `HealthAlert`.

---

### 6.2. Critical Failures

- If `camera_service` fails:
  - Attempt automatic restart (N times).
  - If still failing:
    - TTS: “Camera lỗi, vui lòng khởi động lại kính.”
    - Send `alert` via `io_hub` to User App/Family App.

- If `io_hub` loses connection to User App:
  - Enter offline mode:
    - Disable voice AI and route updates.
    - Continue local safety and basic logging.
  - Show limited status in TTS when user interacts.

---

### 6.3. Data Persistence

- Config:
  - Stored in local config file (e.g., `/etc/ai-glasses/config.yaml`).
  - Includes mode preferences, familiar places, TTS settings.
- Logs:
  - Rotating log files to avoid full disk.
  - Logs from each service tagged with `service_name`.

---

## 7. Performance Targets

All numbers are **targets** and must be verified by benchmarks in `tests/perf/`.

### 7.1. Navigation/Danger Mode

- Effective object/danger updates: **4–6 Hz**.
- Worst-case processing time per frame: **< 150 ms**.
- TTS start after danger detection: **< 400 ms**.

### 7.2. OCR Mode

- Single-scene OCR latency: **< 1.5 s** from capture to spoken result (typical).

### 7.3. Face Recognition

- Latency: **< 1 s** to announce presence of a known person in view.

### 7.4. Resource Usage

- CPU:
  - Maintain headroom (e.g. keep average CPU usage < 80%) to avoid overheating.
- Memory:
  - Fit within Pi Zero 2 W constraints; avoid fragmentation and leaks.
- Temperature:
  - CPU temperature under **80°C** in normal operation.

---

## 8. Development & Testing Notes

- Each service should:
  - Have a small standalone test harness.
  - Support mock event bus for unit tests.
- Integration tests:
  - Simulate typical user flows:
    - Walking with navigation.
    - Reading price tags.
    - Face recognition at home.
    - Offline mode and recovery.

---

_End of document_
