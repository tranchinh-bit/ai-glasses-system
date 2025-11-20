# 05 – Mobile Family App Design (Monitoring App)

## 1. Goals

The Family App allows family members to:

- Monitor the user’s location periodically.
- Receive SOS and other critical alerts.
- Optionally send destinations or suggestions to glasses indirectly via backend.

---

## 2. Architecture Overview

Main components:

1. **BackendClient**
   - Connects to backend via:
     - REST (for historical data).
     - WebSocket (for realtime updates).
2. **UI Layer**
   - Map screen:
     - Shows latest known location of the user.
   - Alerts screen:
     - Lists SOS & health alerts.
   - RouteToUser screen:
     - Provides navigation to user’s location (using phone’s map).
   - Settings screen:
     - Manage which user/device to monitor.

3. **Data Layer**
   - Stores:
     - Linked user IDs / device IDs.
     - Local copies of recent alerts & locations.

---

## 3. Core Flows

### 3.1. Realtime Location Updates

- Backend pushes location updates via WebSocket at least every 30 minutes per device.
- Family App:
  - Updates map marker position.
  - Displays timestamp and accuracy.

### 3.2. SOS Handling

- When an SOS alert arrives:
  - Immediately show a full-screen notification or system notification.
  - Show:
    - Time of SOS.
    - Location on map.
  - Provide button:
    - “Chỉ đường tới đây” → opens native map app with directions.

### 3.3. Device Selection

- If a family member monitors multiple devices (e.g., multiple users):
  - Provide list of devices.
  - Select active device to display on map.

---

## 4. Security & Privacy

- Authentication:
  - Family user must log in (account/password/OAuth).
- Authorization:
  - Only devices linked to the family account can be monitored.
- Data handling:
  - Location & alerts must be transferred over HTTPS/WSS.
  - Provide an option to clear local history on device.

---

## 5. Performance

- WebSocket connection should be kept alive with minimal traffic.
- Map updates are event-driven (no constant polling).
- Cache recent location to avoid blank map in case of temporary disconnect.
