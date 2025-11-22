# Models – AI Glasses

Thư mục này chỉ chứa **meta thông tin** về model (tên, đường dẫn, loại, link download), không nhất thiết commit các file model nặng vào repo.

## manifest_pi.yaml

- Liệt kê các model **nhẹ** dùng trên Raspberry Pi Zero 2W.
- Ví dụ:
  - `yolo_v8n_int8.tflite` – detection cơ bản.
  - `depth_lite.tflite` – ước lượng độ sâu đơn giản.
  - `face_recognition.onnx` – embedding khuôn mặt.

## manifest_phone.yaml

- Liệt kê các model **nặng hơn** chạy trên điện thoại:
  - `yolo_v8s_fp16.tflite` hoặc TensorRT / NNAPI.
  - Model OCR, ASR (nếu dùng).
  - Model translation.

## Quy trình sử dụng

1. Dev cập nhật `manifest_*.yaml` với:
   - Tên model.
   - Phiên bản.
   - Link download (Google Drive, S3, v.v.).
2. Script cài đặt trên Pi / App sẽ đọc manifest:
   - Kiểm tra model đã tồn tại chưa.
   - Nếu chưa có:
     - Tải về (nếu được).
     - Hoặc hiển thị hướng dẫn cho người dùng chép model bằng tay.
