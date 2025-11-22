#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PI_CORE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_DIR="${PI_CORE_DIR}/data/logs"

TS=$(date +"%Y%m%d_%H%M%S")
OUT_FILE="${PI_CORE_DIR}/logs_bundle_${TS}.tar.gz"

mkdir -p "${LOG_DIR}"

echo "[*] Collecting logs from ${LOG_DIR}..."
tar -czf "${OUT_FILE}" -C "${LOG_DIR}" .

echo "[+] Logs bundled at: ${OUT_FILE}"
