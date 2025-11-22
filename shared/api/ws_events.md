# WebSocket Events

## 1. Family App <–> Backend

**URL**: `wss://api.ai-glasses.example.com/ws/family`

Events (server → client):

- `location_update`
  - Payload: `LocationRecord` (JSON as per OpenAPI).
- `alert_added`
  - Payload: `AlertRecord`.

Events (client → server):

- `subscribe_device`
  - Payload: `{ "device_id": "glasses_001" }`
- `unsubscribe_device`
  - Payload: `{ "device_id": "glasses_001" }`

## 2. User App <–> Glasses

**URL (example)**: `ws://<glasses_ip>:9000/ws`

- Payload always is **binary Protobuf `Envelope`** (defined in `messages.proto`).
- No extra JSON wrapper.
- Heartbeat:
  - client → server: `Envelope{ heartbeat: { ... } }`
  - server → client: optional `Envelope{ heartbeat: { ... } }`
