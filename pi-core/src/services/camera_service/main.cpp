#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>

int main() {
    cv::VideoCapture cap0(0);
    if (!cap0.isOpened()) {
        std::cerr << "Cannot open camera 0\n";
        return 1;
    }

    cv::Mat frame;
    int frames = 0;
    auto start = std::chrono::steady_clock::now();

    while (true) {
        if (!cap0.read(frame)) break;
        frames++;
        auto now = std::chrono::steady_clock::now();
        double sec = std::chrono::duration<double>(now - start).count();
        if (sec >= 5.0) {
            std::cout << "FPS: " << frames / sec << std::endl;
            frames = 0;
            start = now;
        }
        // Không hiển thị để tiết kiệm tài nguyên
        if (cv::waitKey(1) == 27) break;
    }
    return 0;
}
