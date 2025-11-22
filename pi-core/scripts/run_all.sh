#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PI_CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PI_CORE_DIR}"

# Activate venv
source .venv/bin/activate

LOG_DIR="${PI_CORE_DIR}/data/logs"
mkdir -p "${LOG_DIR}"

echo "[*] Starting camera_service..."
# Giả sử binary build ra tại build/src/services/camera_service/camera_service
"${PI_CORE_DIR}/build/src/services/camera_service/camera_service" \
  >> "${LOG_DIR}/camera_service.log" 2>&1 &

CAMERA_PID=$!

echo "[*] Starting Python orchestrator..."
python -m src.main >> "${LOG_DIR}/core.log" 2>&1 &

CORE_PID=$!

echo "[+] ai-glasses-core started. PIDs: camera=${CAMERA_PID}, core=${CORE_PID}"

wait
