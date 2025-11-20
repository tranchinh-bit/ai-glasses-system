# AI Glasses System – Documentation

This `docs/` directory contains the **core design specifications** for the AI Glasses System, including:

- High-level architecture
- Protocol & message design (glasses ↔ phone ↔ backend)
- Pi Zero 2W core architecture & vision algorithms
- Mobile apps (user & family)
- Cloud backend (optional)
- Power & health management
- Implementation roadmap

> **Key constraint:**  
> The device uses **Raspberry Pi Zero 2W** as CPU, so **all designs are optimized** for:
> - Low CPU usage
> - Low RAM usage (512MB)
> - Low latency for safety-critical tasks
> - Heavy offloading to the smartphone whenever possible

## Document Index

1. [00-system-overview.md](00-system-overview.md)  
2. [01-protocol-and-messages.md](01-protocol-and-messages.md)  
3. [02-pi-core-architecture.md](02-pi-core-architecture.md)  
4. [03-pi-vision-algorithms.md](03-pi-vision-algorithms.md)  
5. [04-mobile-user-app-design.md](04-mobile-user-app-design.md)  
6. [05-mobile-family-app-design.md](05-mobile-family-app-design.md)  
7. [06-cloud-backend-design.md](06-cloud-backend-design.md)  
8. [07-power-and-health-management.md](07-power-and-health-management.md)  
9. [08-roadmap-and-phasing.md](08-roadmap-and-phasing.md)

## Conventions

- Pi Zero 2W side is referred to as **“glasses”** or **“pi-core”**.
- User smartphone is **“User App” / App A**.
- Family smartphone is **“Family App” / App B**.
- Cloud server is **“backend”** (optional but recommended).
- Messages between components **must** follow the protocol in `shared/` (see `01-protocol-and-messages.md` for the logical spec).

All later code in `pi-core/`, `mobile/`, and `cloud-backend/` must conform to these design docs.
