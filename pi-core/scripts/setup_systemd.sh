#!/usr/bin/env bash
set -e

SERVICE_NAME="ai-glasses-core.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_NAME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PI_CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[*] Creating systemd service at ${SERVICE_PATH}..."

sudo bash -c "cat > ${SERVICE_PATH}" <<EOF
[Unit]
Description=AI Glasses Core Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=${PI_CORE_DIR}
ExecStart=/bin/bash -lc '${PI_CORE_DIR}/scripts/run_all.sh'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "[*] Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"

echo "[+] Done. You can start with: sudo systemctl start ${SERVICE_NAME}"
