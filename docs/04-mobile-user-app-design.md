# 04 – Mobile User App Design (User-side Phone)

## 1. Goals

The User App is the smartphone app used by the **glasses owner**. It must:

- Connect reliably to the glasses over Wi-Fi.
- Provide GPS & route planning.
- Provide STT + LLM-based AI services.
- Integrate OS features (weather, calendar, call, music).
- Offer an accessible UI (TalkBack-friendly) for visually impaired users.

---

## 2. Architecture Overview

Main modules:

1. **GlassesConnectionManager**
   - WebSocket client to the glasses.
   - Encodes/decodes messages using shared Protobuf.
   - Manages reconnection, heartbeats.

2. **VoiceService**
   - Receives `voice_request` from glasses.
   - Runs STT (cloud or on-device).
   - Calls LLM API with context:
     - user question
     - optional `context_snapshot` data from glasses
   - Generates natural-language answer & sends back as `voice_reply`.

3. **NavigationService**
   - Uses phone GPS + map SDK (e.g., Google Maps).
   - Calculates routes to saved places or arbitrary destinations.
   - Converts route into discrete steps:
     - Distance, direction, street name, spoken hint.
   - Sends `navigation_step` messages to glasses.

4. **OS Integration Services**
   - WeatherService:
     - Calls weather API, returns text summary.
   - CalendarService:
     - Reads today’s events from system calendar.
   - CallService:
     - Initiates phone calls (with user confirmation).
   - MusicService:
     - Integrates with a music player or streaming app.

5. **UI Layer**
   - Accessible screens:
     - Home/Status
     - Places management
     - Faces management
     - Settings
     - Debug (for development).

6. **Data Layer**
   - Stores:
     - Saved places (synced with backend and glasses).
     - Known glasses devices (IP, ID).
     - User account and preferences.

---

## 3. Core Flows

### 3.1. Connection to Glasses

- User selects:
  - Glasses IP (or uses discovery/QR).
  - Device ID.
- App opens WebSocket connection:
  - `ws://<glasses_ip>:<port>/ws`.
- On connect:
  - Perform version handshake.
  - Start receiving `status_update`, `alert`, etc.

### 3.2. Handling Voice Requests

1. Glasses sends `voice_request` with audio chunks.
2. VoiceService:
   - Reconstructs full audio stream if multiple chunks.
   - Run STT (speech-to-text) with language `vi-VN`.
3. Build LLM prompt including:
   - User’s transcript.
   - Latest `context_snapshot` (if available).
4. Call LLM (cloud or local).
5. Receive model reply → text (Vietnamese).
6. Send `voice_reply` back to glasses via GlassesConnectionManager.

### 3.3. Navigation / GPS

1. User or family sets a destination:
   - A saved place.
   - A map point.
2. NavigationService:
   - Reads current GPS location.
   - Uses map service to compute a route.
   - Splits route into steps:
     - Each step → approx distance + direction + street name.
3. For each step:
   - Send `navigation_step` to glasses with an appropriate `spoken_hint`.
4. Optional:
   - Wait for confirmation or responses from glasses (e.g., “step reached”).

### 3.4. Saved Places Management

- User can:
  - Save current location as a named place.
  - Edit or delete saved places.
- App ensures consistency:
  - Update local DB.
  - Sync with backend.
  - Send `place_update` to glasses.

---

## 4. Accessibility Requirements

- Design UI with:
  - Large touch targets.
  - High contrast colors.
  - Clear labels, using Android accessibility APIs.
- All essential controls must be reachable via TalkBack navigation.
- Avoid information-dense layouts; prefer simple, linear flows.

---

## 5. Error Handling

- If connection to glasses is lost:
  - Show clear status.
  - Provide option to retry.
- If STT or LLM fails:
  - Fallback:
    - “Em không nghe rõ, xin hãy thử lại.”
- If GPS is off or location permission denied:
  - Prompt user to enable/allow.

---

## 6. Performance & Security

- Keep WebSocket connection alive but low-traffic:
  - Heartbeat/ping messages at low frequency.
- Use TLS for LLM & API calls.
- Use authentication tokens to access backend and LLM APIs.
- Be careful with battery consumption:
  - Throttle GPS usage (e.g., every X seconds/minutes).
  - Release resources when app is in background as appropriate.
