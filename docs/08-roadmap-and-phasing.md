# 08 – Roadmap & Phasing

This document maps the **implementation phases** of the project.

---

## Phase 1 – Documentation (CURRENT)

- Define:
  - System overview.
  - Protocol & messages.
  - Pi-core architecture.
  - Vision algorithms.
  - Mobile app designs.
  - Backend design.
  - Power & health strategies.
- Output: all documents in `docs/`.

---

## Phase 2 – Shared Protocol & Models (`shared/`)

- Implement:
  - Protobuf definitions (`messages.proto`, `enums.proto`).
  - OpenAPI spec for backend REST.
  - Configuration templates (power profiles, danger rules, traffic rules).
- Generate code:
  - For Pi (C++/Python).
  - For User App (Kotlin/Java).
  - For Family App.
  - For backend.

---

## Phase 3 – Pi Core Implementation (`pi-core/`)

- Implement:
  - `camera_service` with shared memory ring buffer.
  - `vision_object_danger` + trackers + danger logic.
  - `fusion_engine` and `core_orchestrator`.
  - `io_hub` WebSocket client.
  - `power_manager` and `health_monitor`.
- Later:
  - Add OCR, currency, face recognition.

Test:

- Performance (FPS, latency).
- Stability (long runs).

---

## Phase 4 – Mobile Apps (`mobile/`)

- User App:
  - Implement GlassesConnectionManager.
  - Implement VoiceService with STT + LLM.
  - Implement NavigationService (GPS + routes).
  - Implement OS integration features.
  - Build accessible UI.

- Family App:
  - Implement backend connection.
  - Map screen + alerts handling.

---

## Phase 5 – Backend (`cloud-backend/`) + Integration

- Implement REST + WebSocket backend.
- Hook up:
  - User App → backend (location, alerts).
  - Family App → backend (monitoring).
- Perform end-to-end tests:
  - Glasses ↔ User App ↔ Backend ↔ Family App.

---

Each phase should be **incrementally testable**:  
Even with only pi-core & User App (no backend), glasses and user can already use most local features (danger detection, OCR, navigation with direct phone).
