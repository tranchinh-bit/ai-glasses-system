# AI Glasses Protocol – Protobuf

Thư mục này định nghĩa **protocol dùng chung** giữa:

- Pi (pi-core – Python).
- Mobile apps (Android – Kotlin/Java).
- Cloud backend (Python).

## Cấu trúc

- `enums.proto`: các enum dùng chung (OffloadMode, EventType, DangerLevel, v.v.).
- `messages.proto`: định nghĩa messages chính, dùng import `enums.proto`.
- `gen/python/`: mã sinh ra cho Python (aiglasses_pb2.py, v.v.).
- `gen/java/`: mã sinh ra cho Android (file .java tương ứng).

## Cách generate code

Yêu cầu cài:

- `protoc` (Protocol Buffers compiler).
- `protoc-gen-python` (thường đi kèm với `protobuf` Python).
- `protoc-gen-java` (kèm protoc).

Từ thư mục gốc repo:

```bash
cd shared/tools
./generate_protos.sh
