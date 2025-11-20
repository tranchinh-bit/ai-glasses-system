# 00 – System Overview

## 1. System Goals

The AI Glasses System is designed for **visually impaired users** with the following objectives:

1. **Real-time perception with AI** on Pi Zero 2W:
   - Object detection in real life.
   - Text & number recognition (Vietnamese), reading left→right.
   - Vietnamese currency denomination recognition.
   - Obstacle & danger detection while walking.
   - Familiar face recognition.
   - Vietnamese traffic scene understanding (lights, signs, crosswalks, lanes).

2. **AI-powered interaction**:
   - Glasses proactively warn about dangers.
   - Glasses answer simple questions via voice (with help from smartphone & LLM).

3. **Navigation & GPS**:
   - Use smartphone GPS + maps to compute routes.
   - Save favorite places and navigate by name.
   - Share location with family every 30 minutes.

4. **Smartphone integration**:
   - Strong link to user’s phone: weather, calendar, call, music, etc.
   - User App (for the glasses user).
   - Family App (for remote monitoring).

5. **Safety & emergency**:
   - HX1838 IR module + physical remote buttons for critical actions (SOS, mode switch, etc.).
   - SOS alerts to family with location.

6. **Energy efficiency & robustness**:
   - Intelligent power profiles.
   - Continuous health monitoring (temperature, CPU, RAM, camera, Wi-Fi).
   - Fail-safe behavior when something goes wrong.

---

## 2. High-Level Architecture

Top-level repo structure:

```text
ai-glasses-system/
├── docs/           # Design docs (this folder)
├── shared/         # Shared protocol, message formats, model specs, configs
├── pi-core/        # Runtime on Raspberry Pi Zero 2W (glasses)
├── mobile/
│   ├── user-app/   # Smartphone app for user
│   └── family-app/ # Smartphone app for family monitoring
└── cloud-backend/  # Optional backend for location & alerts
