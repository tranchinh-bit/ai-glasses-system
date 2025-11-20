# Shared Protocol

This folder contains Protobuf definitions for **all messages** exchanged between:

- Glasses (Pi Zero 2W – `pi-core`)
- User App (mobile/user-app)
- Family App (mobile/family-app)
- Cloud Backend (cloud-backend)

All components **must** generate code from the same `.proto` files to guarantee:

- High performance (binary, compact).
- Type safety.
- No schema drift between services.

Main files:

- `enums.proto` – shared enums.
- `messages.proto` – top-level `Envelope` + all message types.
