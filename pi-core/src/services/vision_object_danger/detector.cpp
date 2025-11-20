#include <opencv2/opencv.hpp>
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/kernels/register.h"

#include "detector.h"

Detector::Detector(const std::string& model_path, float score_thresh, float iou_thresh)
    : score_thresh_(score_thresh), iou_thresh_(iou_thresh)
{
    model_ = tflite::FlatBufferModel::BuildFromFile(model_path.c_str());
    if (!model_) {
        throw std::runtime_error("Failed to load TFLite model");
    }

    tflite::ops::builtin::BuiltinOpResolver resolver;
    tflite::InterpreterBuilder(*model_, resolver)(&interpreter_);

    interpreter_->AllocateTensors();
    input_tensor_ = interpreter_->input_tensor(0);

    input_h_ = input_tensor_->dims->data[1];
    input_w_ = input_tensor_->dims->data[2];

    output_tensor_ = interpreter_->output_tensor(0);
}

cv::Mat Detector::preprocess(const cv::Mat& img)
{
    cv::Mat resized;
    cv::resize(img, resized, cv::Size(input_w_, input_h_));
    resized.convertTo(resized, CV_32FC3, 1 / 255.0);
    return resized;
}

std::vector<Detection> Detector::detect(const cv::Mat& frame)
{
    cv::Mat input = preprocess(frame);
    float* input_data = interpreter_->typed_input_tensor<float>(0);
    memcpy(input_data, input.data, input.total() * input.elemSize());

    interpreter_->Invoke();

    float* output = interpreter_->typed_output_tensor<float>(0);

    // YOLOv8 format output: [batch, N, 6] = [x, y, w, h, score, class]
    std::vector<Detection> dets;

    const int num_det = output_tensor_->dims->data[1];
    const int stride = 6;

    for (int i = 0; i < num_det; i++)
    {
        float x = output[i * stride + 0];
        float y = output[i * stride + 1];
        float w = output[i * stride + 2];
        float h = output[i * stride + 3];
        float score = output[i * stride + 4];
        int cls = static_cast<int>(output[i * stride + 5]);

        if (score < score_thresh_) continue;

        float x0 = (x - w / 2.0f) * frame.cols;
        float y0 = (y - h / 2.0f) * frame.rows;
        float x1 = (x + w / 2.0f) * frame.cols;
        float y1 = (y + h / 2.0f) * frame.rows;

        dets.push_back({
            cv::Rect2f(cv::Point2f(x0, y0), cv::Point2f(x1, y1)),
            score,
            cls
        });
    }

    return non_max_suppression(dets);
}

std::vector<Detection> Detector::non_max_suppression(std::vector<Detection>& dets)
{
    std::vector<Detection> results;
    std::sort(dets.begin(), dets.end(),
              [](auto& a, auto& b) { return a.score > b.score; });

    std::vector<bool> removed(dets.size(), false);

    for (size_t i = 0; i < dets.size(); i++)
    {
        if (removed[i]) continue;

        results.push_back(dets[i]);

        for (size_t j = i + 1; j < dets.size(); j++) {
            if (removed[j]) continue;

            float iou = (dets[i].bbox & dets[j].bbox).area() /
                        (dets[i].bbox | dets[j].bbox).area();

            if (iou > iou_thresh_) {
                removed[j] = true;
            }
        }
    }

    return results;
}
