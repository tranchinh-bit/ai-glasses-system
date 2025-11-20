#!/usr/bin/env bash
#
# generate_protos.sh
# Script sinh code từ các file .proto dùng chung cho pi-core (Python)
# và mobile (Java/Kotlin).
#
# Chạy:
#   bash shared/tools/generate_protos.sh

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SHARED_ROOT="$( cd "${SCRIPT_DIR}/.." && pwd )"

PROTO_SRC_DIR="${SHARED_ROOT}/protocol"
PY_OUT_DIR="${PROTO_SRC_DIR}/gen/python"
JAVA_OUT_DIR="${PROTO_SRC_DIR}/gen/java"

echo "[PROTO] Shared root   : ${SHARED_ROOT}"
echo "[PROTO] Proto src dir : ${PROTO_SRC_DIR}"
echo "[PROTO] Python out    : ${PY_OUT_DIR}"
echo "[PROTO] Java out      : ${JAVA_OUT_DIR}"

mkdir -p "${PY_OUT_DIR}"
mkdir -p "${JAVA_OUT_DIR}"

PROTO_FILES=(
  "enums.proto"
  "messages.proto"
)

if ! command -v protoc >/dev/null 2>&1; then
  echo "ERROR: 'protoc' not found."
  echo "Install Protobuf compiler before running this script."
  exit 1
fi

echo "[PROTO] Generating Python & Java code..."

protoc \
  -I "${PROTO_SRC_DIR}" \
  --python_out="${PY_OUT_DIR}" \
  --java_out="${JAVA_OUT_DIR}" \
  "${PROTO_FILES[@]}"

echo "[PROTO] Done."
echo "  Python: ${PY_OUT_DIR}"
echo "  Java  : ${JAVA_OUT_DIR}"
