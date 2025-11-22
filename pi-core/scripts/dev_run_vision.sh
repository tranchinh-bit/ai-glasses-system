#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PI_CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PI_CORE_DIR}"

source .venv/bin/activate

echo "[*] Running vision_local engine in debug mode..."
python -m src.services.vision_local.engine --debug
