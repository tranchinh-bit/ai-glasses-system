// pi-core/src/vision_object_danger/danger_analyzer.cpp
#include "danger_analyzer.hpp"

#include <algorithm>
#include <cmath>

namespace vision {

DangerAnalyzer::DangerAnalyzer(float danger_distance_thresh_m,
                               float front_angle_center_deg,
                               float front_angle_half_width_deg,
                               int   min_consecutive_frames)
    : danger_distance_thresh_m_(danger_distance_thresh_m),
      front_angle_center_deg_(front_angle_center_deg),
      front_angle_half_width_deg_(front_angle_half_width_deg),
      min_consecutive_frames_(min_consecutive_frames) {}

std::vector<DangerEvent> DangerAnalyzer::analyze(
        const std::vector<TrackedObject>& tracks) {

    std::vector<DangerEvent> events;
    events.reserve(tracks.size());

    for (const auto& tr : tracks) {
        if (!is_in_front(tr.angle_deg)) {
            reset_counter(tr.track_id);
            continue;
        }

        if (tr.distance_m <= 0.0f) {
            reset_counter(tr.track_id);
            continue;
        }

        bool approaching = is_approaching(tr);
        if (!approaching) {
            reset_counter(tr.track_id);
            continue;
        }

        if (tr.distance_m <= danger_distance_thresh_m_) {
            int count = ++consecutive_front_frames_[tr.track_id];

            if (count >= min_consecutive_frames_) {
                DangerEvent ev;
                ev.track_id    = tr.track_id;
                ev.class_id    = tr.class_id;
                ev.distance_m  = tr.distance_m;
                ev.angle_deg   = tr.angle_deg;
                ev.level       = DangerLevel::HIGH;
                events.push_back(ev);
            }
        } else {
            reset_counter(tr.track_id);
        }
    }

    return events;
}

bool DangerAnalyzer::is_in_front(float angle_deg) const {
    float left  = front_angle_center_deg_ - front_angle_half_width_deg_;
    float right = front_angle_center_deg_ + front_angle_half_width_deg_;
    return (angle_deg >= left && angle_deg <= right);
}

bool DangerAnalyzer::is_approaching(const TrackedObject& tr) {
    auto it = last_distance_.find(tr.track_id);
    if (it == last_distance_.end()) {
        last_distance_[tr.track_id] = tr.distance_m;
        return false; // chưa có frame trước để so
    }

    float prev = it->second;
    it->second = tr.distance_m;

    // nếu giảm hơn 5cm / frame coi như đang tiến lại gần
    return (prev - tr.distance_m) > 0.05f;
}

void DangerAnalyzer::reset_counter(int track_id) {
    consecutive_front_frames_.erase(track_id);
    last_distance_.erase(track_id);
}

} // namespace vision
