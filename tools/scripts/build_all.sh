#!/usr/bin/env bash
set -euo pipefail

# Thư mục gốc repo: ai-glasses-system/
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"

echo "[BUILD] Repo root: ${ROOT_DIR}"

echo "[BUILD] 1) Generate protobuf (shared/protocol)..."
bash "${ROOT_DIR}/shared/tools/generate_protos.sh"

echo "[BUILD] 2) Build cloud-backend Docker image..."
docker build -t aiglasses-backend "${ROOT_DIR}/cloud-backend"

echo "[BUILD] Hoàn tất."
echo "  - Image backend: aiglasses-backend"
echo "  - Protobuf: shared/protocol/gen/{python,java}"
