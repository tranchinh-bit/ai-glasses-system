package com.ai_glasses.userapp

import android.util.Log

/**
 * Stub VisionEngine chạy YOLO trên phone.
 * Sau này bạn load model TFLite và chạy thật tại đây.
 */
class VisionEngine {

    fun processFrame(jpeg: ByteArray): String {
        // TODO: decode JPEG, resize, chạy TFLite...
        Log.d("VisionEngine", "processFrame called, size=${jpeg.size}")
        // Trả JSON giả lập detection_result
        return """{"type":"detection_result","items":[]}"""
    }
}
