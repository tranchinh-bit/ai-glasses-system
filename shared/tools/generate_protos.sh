#!/usr/bin/env bash
set -e

# Script generate mã protobuf cho Python và Java.
# Chạy từ thư mục shared/tools hoặc từ root (có điều chỉnh path).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROTO_DIR="${ROOT_DIR}/shared/protocol"
GEN_PY_DIR="${PROTO_DIR}/gen/python"
GEN_JAVA_DIR="${PROTO_DIR}/gen/java"

mkdir -p "${GEN_PY_DIR}"
mkdir -p "${GEN_JAVA_DIR}"

echo "[*] Root dir: ${ROOT_DIR}"
echo "[*] Proto dir: ${PROTO_DIR}"

cd "${PROTO_DIR}"

echo "[*] Generating Python code..."
protoc \
  --proto_path="${PROTO_DIR}" \
  --python_out="${GEN_PY_DIR}" \
  enums.proto messages.proto

echo "[*] Generating Java code..."
protoc \
  --proto_path="${PROTO_DIR}" \
  --java_out="${GEN_JAVA_DIR}" \
  enums.proto messages.proto

echo "[+] Done. Generated files:"
echo "  Python: ${GEN_PY_DIR}"
echo "  Java  : ${GEN_JAVA_DIR}"
