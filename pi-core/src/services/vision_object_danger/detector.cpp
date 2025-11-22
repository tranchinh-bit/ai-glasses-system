// pi-core/src/vision_object_danger/detector.cpp
#include "detector.hpp"

#include <algorithm>
#include <cmath>

namespace vision {

namespace {

float IoU(const BBox& a, const BBox& b) {
    float inter_x1 = std::max(a.x1, b.x1);
    float inter_y1 = std::max(a.y1, b.y1);
    float inter_x2 = std::min(a.x2, b.x2);
    float inter_y2 = std::min(a.y2, b.y2);

    float inter_w = std::max(0.0f, inter_x2 - inter_x1);
    float inter_h = std::max(0.0f, inter_y2 - inter_y1);
    float inter_area = inter_w * inter_h;

    float area_a = std::max(0.0f, (a.x2 - a.x1)) *
                   std::max(0.0f, (a.y2 - a.y1));
    float area_b = std::max(0.0f, (b.x2 - b.x1)) *
                   std::max(0.0f, (b.y2 - b.y1));

    float union_area = area_a + area_b - inter_area;
    if (union_area <= 0.0f) return 0.0f;
    return inter_area / union_area;
}

inline void compute_center(const BBox& box, float& cx, float& cy) {
    cx = 0.5f * (box.x1 + box.x2);
    cy = 0.5f * (box.y1 + box.y2);
}

// 1 camera FOV 140° → 0° ở mép trái, 140° ở mép phải
inline float compute_angle_deg(float cx,
                               int   img_width,
                               float fov_deg) {
    float norm_x = cx / static_cast<float>(img_width); // [0,1]
    return norm_x * fov_deg;                          // [0,fov_deg]
}

} // namespace

Detector::Detector(int img_width,
                   int img_height,
                   float fov_deg,
                   float nms_iou_thresh,
                   float score_thresh)
    : img_width_(img_width),
      img_height_(img_height),
      fov_deg_(fov_deg),
      nms_iou_thresh_(nms_iou_thresh),
      score_thresh_(score_thresh) {}

std::vector<Detection> Detector::postprocess(
        const std::vector<RawDetection>& raw_dets) const {

    // 1. Lọc score
    std::vector<RawDetection> filtered;
    filtered.reserve(raw_dets.size());
    for (const auto& d : raw_dets) {
        if (d.score >= score_thresh_) {
            filtered.push_back(d);
        }
    }

    // 2. Sort theo class + score
    std::vector<RawDetection> sorted = filtered;
    std::sort(sorted.begin(), sorted.end(),
              [](const RawDetection& a, const RawDetection& b) {
                  if (a.class_id == b.class_id) {
                      return a.score > b.score;
                  }
                  return a.class_id < b.class_id;
              });

    // 3. NMS từng class
    std::vector<Detection> result;
    result.reserve(sorted.size());

    size_t i = 0;
    while (i < sorted.size()) {
        int current_class = sorted[i].class_id;

        std::vector<RawDetection> same_class;
        while (i < sorted.size() &&
               sorted[i].class_id == current_class) {
            same_class.push_back(sorted[i]);
            ++i;
        }

        std::vector<bool> suppressed(same_class.size(), false);
        for (size_t m = 0; m < same_class.size(); ++m) {
            if (suppressed[m]) continue;
            const auto& best = same_class[m];

            Detection det;
            det.class_id = best.class_id;
            det.score    = best.score;
            det.bbox     = best.bbox;

            float cx, cy;
            compute_center(det.bbox, cx, cy);
            det.angle_deg  = compute_angle_deg(cx, img_width_, fov_deg_);
            det.distance_m = best.estimated_distance_m;

            result.push_back(det);

            for (size_t n = m + 1; n < same_class.size(); ++n) {
                if (suppressed[n]) continue;
                float iou = IoU(best.bbox, same_class[n].bbox);
                if (iou >= nms_iou_thresh_) {
                    suppressed[n] = true;
                }
            }
        }
    }

    return result;
}

} // namespace vision
