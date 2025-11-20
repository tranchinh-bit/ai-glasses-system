#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
source "${ROOT_DIR}/.venv/bin/activate"

export PYTHONPATH="${ROOT_DIR}/src:${ROOT_DIR}/../shared/protocol/gen/python:${PYTHONPATH}"

cd "${ROOT_DIR}"
echo "[RUN] Starting Pi Core main..."
exec python -m src.main
