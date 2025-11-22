// pi-core/src/vision_object_danger/vision_types.hpp
#pragma once

#include <vector>

namespace vision {

struct BBox {
    float x1{0.0f};
    float y1{0.0f};
    float x2{0.0f};
    float y2{0.0f};
};

struct RawDetection {
    BBox  bbox;
    int   class_id{0};
    float score{0.0f};
    float estimated_distance_m{0.0f}; // khoảng cách ước lượng (m)
};

struct Detection {
    BBox  bbox;
    int   class_id{0};
    float score{0.0f};
    float angle_deg{0.0f};     // góc so với biên trái ảnh
    float distance_m{0.0f};    // khoảng cách ước lượng (m)
};

struct HistoryPoint {
    float x{0.0f};
    float y{0.0f};
};

struct TrackedObject {
    int   track_id{0};
    int   class_id{0};
    float score{0.0f};
    BBox  bbox;
    float angle_deg{0.0f};
    float distance_m{0.0f};
    int   lost_frames{0};

    std::vector<HistoryPoint> history;
};

enum class DangerLevel {
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2
};

struct DangerEvent {
    int   track_id{0};
    int   class_id{0};
    float distance_m{0.0f};
    float angle_deg{0.0f};
    DangerLevel level{DangerLevel::LOW};
};

} // namespace vision
