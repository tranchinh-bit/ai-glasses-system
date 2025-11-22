// pi-core/src/vision_object_danger/tracker.hpp
#pragma once

#include <unordered_map>
#include <vector>
#include "vision_types.hpp"

namespace vision {

class Tracker {
public:
    Tracker(int   max_lost_frames   = 5,
            float iou_match_thresh  = 0.3f,
            float smoothing_alpha   = 0.5f);

    // Cập nhật track từ list detection
    std::vector<TrackedObject> update(
        const std::vector<Detection>& detections);

private:
    int   max_lost_frames_;
    float iou_match_thresh_;
    float smoothing_alpha_;
    int   next_id_;

    std::unordered_map<int, TrackedObject> tracks_;
};

} // namespace vision
