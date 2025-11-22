// pi-core/src/vision_object_danger/danger_analyzer.hpp
#pragma once

#include <unordered_map>
#include <vector>
#include "vision_types.hpp"

namespace vision {

class DangerAnalyzer {
public:
    DangerAnalyzer(float danger_distance_thresh_m   = 3.0f,
                   float front_angle_center_deg     = 70.0f, // giữa FOV 140°
                   float front_angle_half_width_deg = 45.0f,
                   int   min_consecutive_frames     = 3);

    std::vector<DangerEvent> analyze(
        const std::vector<TrackedObject>& tracks);

private:
    bool is_in_front(float angle_deg) const;
    bool is_approaching(const TrackedObject& tr);
    void reset_counter(int track_id);

    float danger_distance_thresh_m_;
    float front_angle_center_deg_;
    float front_angle_half_width_deg_;
    int   min_consecutive_frames_;

    std::unordered_map<int, int>   consecutive_front_frames_;
    std::unordered_map<int, float> last_distance_;
};

} // namespace vision
