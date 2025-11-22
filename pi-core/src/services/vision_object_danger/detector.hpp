// pi-core/src/vision_object_danger/detector.hpp
#pragma once

#include <vector>
#include "vision_types.hpp"

namespace vision {

class Detector {
public:
    Detector(int img_width,
             int img_height,
             float fov_deg,
             float nms_iou_thresh = 0.5f,
             float score_thresh   = 0.4f);

    // Hậu xử lý YOLO: NMS + tính góc + khoảng cách
    std::vector<Detection> postprocess(
        const std::vector<RawDetection>& raw_dets) const;

private:
    int   img_width_;
    int   img_height_;
    float fov_deg_;
    float nms_iou_thresh_;
    float score_thresh_;
};

} // namespace vision
