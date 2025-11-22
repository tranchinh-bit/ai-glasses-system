#!/usr/bin/env bash
set -e

echo "[*] Updating apt..."
sudo apt update
sudo apt upgrade -y

echo "[*] Installing system packages..."
sudo apt install -y \
  git cmake g++ \
  python3 python3-venv python3-pip \
  libcamera-dev libatlas-base-dev \
  libjpeg-dev libopenblas-dev

# Optional: sound utils
sudo apt install -y alsa-utils

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PI_CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[*] Creating Python venv..."
cd "${PI_CORE_DIR}"
python3 -m venv .venv
source .venv/bin/activate

echo "[*] Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[*] Building C++ services..."
mkdir -p build
cd build
cmake ..
make -j2

echo "[+] Install complete."
