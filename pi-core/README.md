# AI Glasses Pi Core

Pi Core chạy trên Raspberry Pi Zero 2W:

- Đọc camera kép, chạy mô hình nhận dạng (YOLO, depth…)
- Phân tích nguy hiểm (`vision_object_danger`)
- Quản lý chế độ nguồn, health, IR remote
- Giao tiếp với mobile app & cloud backend qua WebSocket + REST

## Yêu cầu hệ thống

- Raspberry Pi OS (Lite khuyến nghị)
- Python 3.9+
- OpenCV (tùy chọn nếu dùng camera_service)
- Protobuf >= 3.20
- TFLite runtime (hoặc onnxruntime trong bản onnx)

## Cài đặt nhanh

```bash
cd pi-core/scripts
bash install_pi.sh
