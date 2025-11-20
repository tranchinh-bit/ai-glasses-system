#include "tracker.h"

int Tracker::next_id_ = 1;

std::vector<Track> Tracker::update(const std::vector<Detection>& detections)
{
    // Update existing tracks
    for (auto& tr : tracks_) {
        tr.matched = false;
    }

    const float DIST_THRESHOLD = 60.0f; // pixels, tune depending on FOV

    for (const auto& det : detections)
    {
        int best_id = -1;
        float best_dist = 1e9;

        cv::Point2f dc(det.bbox.x + det.bbox.width * 0.5f,
                       det.bbox.y + det.bbox.height * 0.5f);

        for (auto& tr : tracks_)
        {
            cv::Point2f tc(tr.bbox.x + tr.bbox.width * 0.5f,
                           tr.bbox.y + tr.bbox.height * 0.5f);

            float dist = cv::norm(dc - tc);
            if (dist < best_dist && dist < DIST_THRESHOLD) {
                best_dist = dist;
                best_id = tr.id;
            }
        }

        if (best_id != -1) {
            // Match with existing track
            for (auto& tr : tracks_) {
                if (tr.id == best_id) {
                    tr.bbox = det.bbox;
                    tr.cls = det.cls;
                    tr.score = det.score;
                    tr.matched = true;
                    tr.age++;
                }
            }
        }
        else {
            // Create new track
            Track new_tr;
            new_tr.id = next_id_++;
            new_tr.bbox = det.bbox;
            new_tr.cls = det.cls;
            new_tr.score = det.score;
            new_tr.age = 1;
            new_tr.matched = true;
            tracks_.push_back(new_tr);
        }
    }

    // Remove old tracks
    tracks_.erase(
        std::remove_if(tracks_.begin(), tracks_.end(),
                       [](const Track& t) { return !t.matched && t.age > 2; }),
        tracks_.end()
    );

    return tracks_;
}
