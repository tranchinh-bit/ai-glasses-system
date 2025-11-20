#include "danger_analyzer.h"
#include <cmath>

HazardResult DangerAnalyzer::analyze(const std::vector<Track>& tracks,
                                     int frame_w, int frame_h)
{
    HazardResult result;
    result.has_danger = false;

    const float FOV_DEG = 140.0f;
    const float CENTER = frame_w / 2.0f;

    for (const auto& tr : tracks)
    {
        float cx = tr.bbox.x + tr.bbox.width / 2.0f;
        float cy = tr.bbox.y + tr.bbox.height / 2.0f;

        float rel_x = (cx - CENTER) / CENTER;
        float angle = rel_x * (FOV_DEG / 2.0f);

        float distance_m = estimate_distance(tr.bbox, frame_w, frame_h);

        // Rule: bất cứ vật thể nào < 2.5m nằm phía trước sẽ báo hazard
        if (distance_m < 2.5f)
        {
            result.has_danger = true;
            result.angle_deg = angle;
            result.distance_m = distance_m;
            result.track_id = tr.id;

            if (distance_m < 1.5f)
                result.severity = "high";
            else
                result.severity = "medium";

            return result;  // trả về ngay hazard đầu tiên
        }
    }

    return result;
}

float DangerAnalyzer::estimate_distance(const cv::Rect2f& box, int w, int h)
{
    float rel_size = box.height / h;
    float dist = 1.0f / (rel_size + 0.01f);
    return dist * 1.2f;
}
