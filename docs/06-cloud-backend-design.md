# 06 – Cloud Backend Design (Optional)

## 1. Goals

- Provide a central hub for:
  - Periodic location storage.
  - SOS & device alerts.
  - Communication between User App and Family App.
- Backend is lightweight and can scale for multiple users/devices.

---

## 2. Core Responsibilities

1. **User/Device Management**
   - Map user accounts ↔ glasses devices.
   - Manage which family accounts have access to which user’s data.

2. **Location Service**
   - Accept periodic location updates from User App or glasses.
   - Store locations in DB.
   - Provide query APIs for recent and historical locations.
   - Push updates via WebSocket to Family App.

3. **Alert Service**
   - Accept alerts (e.g., SOS, health issues).
   - Persist them.
   - Push to subscribed Family Apps in realtime.

4. **Routing Suggestions (optional)**
   - Receive remote destination suggestions from Family App.
   - Forward to User App or glasses.

---

## 3. API Overview

### 3.1. REST Endpoints (Examples)

- `POST /api/v1/location/update`
- `GET /api/v1/location/latest?device_id=...`
- `GET /api/v1/location/history?device_id=...&from=...&to=...`
- `POST /api/v1/alerts`
- `GET /api/v1/alerts/recent?device_id=...`

### 3.2. WebSocket Events

For Family App:

- `location_update`
- `alert_added`

---

## 4. Data Model (Simplified)

Entities:

- `User`
- `Device` (glasses)
- `FamilyMember`
- `LocationRecord`
- `AlertRecord`
- Links: `UserFamilyLink`, `UserDeviceLink`.

---

## 5. Security

- Authentication via JWT or OAuth.
- All connections: HTTPS/WSS.
- Authorize every request:
  - Ensure the requesting user has access to `user_id` / `device_id`.

---

## 6. Implementation Notes

- Can be built with:
  - FastAPI / Node.js / Go – any web framework with good WebSocket support.
- DB:
  - PostgreSQL / MySQL / SQLite (for prototype).
- Deployment:
  - Docker container for portability.

Backend is optional, but strongly recommended for **multi-device/multi-family** support and robust monitoring.
