#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"

echo "[STYLE] Repo root: ${ROOT_DIR}"

cd "${ROOT_DIR}/cloud-backend"

if command -v black >/dev/null 2>&1; then
  echo "[STYLE] Running black..."
  black app
else
  echo "[STYLE] black chưa được cài, bỏ qua."
fi

if command -v isort >/dev/null 2>&1; then
  echo "[STYLE] Running isort..."
  isort app
else
  echo "[STYLE] isort chưa được cài, bỏ qua."
fi

echo "[STYLE] Done."
