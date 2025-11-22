// pi-core/src/vision_object_danger/tracker.cpp
#include "tracker.hpp"

#include <algorithm>
#include <cmath>

namespace vision {

namespace {

float iou_boxes(const BBox& a, const BBox& b) {
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

inline void bbox_center(const BBox& b, float& cx, float& cy) {
    cx = 0.5f * (b.x1 + b.x2);
    cy = 0.5f * (b.y1 + b.y2);
}

} // namespace

Tracker::Tracker(int   max_lost_frames,
                 float iou_match_thresh,
                 float smoothing_alpha)
    : max_lost_frames_(max_lost_frames),
      iou_match_thresh_(iou_match_thresh),
      smoothing_alpha_(smoothing_alpha),
      next_id_(1) {}

std::vector<TrackedObject> Tracker::update(
        const std::vector<Detection>& detections) {

    // 1. tăng lost_frames
    for (auto& kv : tracks_) {
        kv.second.lost_frames++;
    }

    // 2. match detection với track bằng IoU
    for (const auto& det : detections) {
        int   best_track_id = -1;
        float best_iou      = 0.0f;

        for (auto& kv : tracks_) {
            auto& tr = kv.second;
            if (tr.class_id != det.class_id) continue;

            float iou = iou_boxes(tr.bbox, det.bbox);
            if (iou > best_iou) {
                best_iou      = iou;
                best_track_id = tr.track_id;
            }
        }

        if (best_track_id >= 0 && best_iou >= iou_match_thresh_) {
            // cập nhật track cũ
            auto& tr = tracks_[best_track_id];
            tr.lost_frames = 0;
            tr.score       = det.score;

            tr.bbox.x1 = smoothing_alpha_ * det.bbox.x1 +
                         (1.0f - smoothing_alpha_) * tr.bbox.x1;
            tr.bbox.y1 = smoothing_alpha_ * det.bbox.y1 +
                         (1.0f - smoothing_alpha_) * tr.bbox.y1;
            tr.bbox.x2 = smoothing_alpha_ * det.bbox.x2 +
                         (1.0f - smoothing_alpha_) * tr.bbox.x2;
            tr.bbox.y2 = smoothing_alpha_ * det.bbox.y2 +
                         (1.0f - smoothing_alpha_) * tr.bbox.y2;

            tr.angle_deg = smoothing_alpha_ * det.angle_deg +
                           (1.0f - smoothing_alpha_) * tr.angle_deg;
            tr.distance_m = smoothing_alpha_ * det.distance_m +
                            (1.0f - smoothing_alpha_) * tr.distance_m;

            float cx, cy;
            bbox_center(tr.bbox, cx, cy);
            tr.history.push_back({cx, cy});

        } else {
            // tạo track mới
            TrackedObject tr;
            tr.track_id    = next_id_++;
            tr.class_id    = det.class_id;
            tr.score       = det.score;
            tr.bbox        = det.bbox;
            tr.angle_deg   = det.angle_deg;
            tr.distance_m  = det.distance_m;
            tr.lost_frames = 0;

            float cx, cy;
            bbox_center(tr.bbox, cx, cy);
            tr.history.push_back({cx, cy});

            tracks_[tr.track_id] = tr;
        }
    }

    // 3. xoá track mất quá lâu
    std::vector<int> to_erase;
    for (const auto& kv : tracks_) {
        if (kv.second.lost_frames > max_lost_frames_) {
            to_erase.push_back(kv.first);
        }
    }
    for (int id : to_erase) {
        tracks_.erase(id);
    }

    // 4. trả list track
    std::vector<TrackedObject> output;
    output.reserve(tracks_.size());
    for (const auto& kv : tracks_) {
        output.push_back(kv.second);
    }
    return output;
}

} // namespace vision
