#pragma once

#include <vector>
#include <cstdint>

// Khung IPC đơn giản: gửi JPEG qua TCP local hoặc UNIX socket.
// Ở đây chỉ khai báo interface, bạn có thể hoàn thiện sau.

struct FramePacket {
    uint32_t width;
    uint32_t height;
    std::vector<uint8_t> jpeg_data;
};
