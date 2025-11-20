
---

## 2. `pi-core/scripts/install_pi.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

echo "[INSTALL] Updating apt..."
sudo apt-get update

echo "[INSTALL] Installing system deps..."
sudo apt-get install -y python3 python3-pip python3-venv \
  git libatlas-base-dev libopenblas-dev libjpeg-dev zlib1g-dev \
  libavformat-dev libavcodec-dev libavutil-dev libswscale-dev \
  libprotobuf-dev protobuf-compiler

echo "[INSTALL] Creating venv..."
python3 -m venv "${ROOT_DIR}/.venv"
source "${ROOT_DIR}/.venv/bin/activate"

echo "[INSTALL] Installing Python deps..."
pip install --upgrade pip
pip install opencv-python==4.9.0.80 \
            aiohttp==3.9.5 \
            pyyaml==6.0.2 \
            protobuf==4.25.3 \
            numpy==1.26.4

# TFLite runtime (phiên bản nhẹ cho Pi; có thể điều chỉnh theo OS)
echo "[INSTALL] Installing tflite-runtime..."
pip install tflite-runtime==2.14.0 || true

echo "[INSTALL] Done."

echo ""
echo "To run:"
echo "  source ${ROOT_DIR}/.venv/bin/activate"
echo "  python -m src.main"
