#!/usr/bin/env bash
set -e

# Script sync các file config dùng chung sang pi-core & mobile
# để tránh copy tay.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

SHARED_CONFIGS="${ROOT_DIR}/shared/configs"
PI_CONFIGS="${ROOT_DIR}/pi-core/configs"
MOBILE_USER_ASSETS="${ROOT_DIR}/mobile/user-app/app/src/main/assets/configs"

echo "[*] Root dir: ${ROOT_DIR}"

# Đảm bảo thư mục tồn tại
mkdir -p "${PI_CONFIGS}"
mkdir -p "${MOBILE_USER_ASSETS}"

echo "[*] Syncing configs to pi-core..."
cp -v "${SHARED_CONFIGS}/"*.yaml "${PI_CONFIGS}/"

echo "[*] Syncing configs to mobile/user-app assets..."
cp -v "${SHARED_CONFIGS}/"*.yaml "${MOBILE_USER_ASSETS}/"

echo "[+] Done syncing configs."
