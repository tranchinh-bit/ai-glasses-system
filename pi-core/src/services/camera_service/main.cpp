#include <iostream>
#include <chrono>
#include <thread>

// TODO: include libcamera và IPC thực tế.
// Hiện tại in log giả lập frame capture.

int main() {
    std::cout << "[camera_service] started (mock version)." << std::endl;

    while (true) {
        // TODO: capture frame bằng libcamera, gửi qua IPC
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    return 0;
}
