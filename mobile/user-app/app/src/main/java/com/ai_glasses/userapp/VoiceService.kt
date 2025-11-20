package com.ai_glasses.userapp

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import java.util.Locale

/**
 * TTS trên điện thoại – dùng để đọc lại hazard hoặc thông báo từ kính nếu muốn.
 */
class VoiceService(context: Context) : TextToSpeech.OnInitListener {

    private var tts: TextToSpeech = TextToSpeech(context, this)
    private var initialized = false

    override fun onInit(status: Int) {
        initialized = status == TextToSpeech.SUCCESS
        if (initialized) {
            val result = tts.setLanguage(Locale("vi", "VN"))
            if (result == TextToSpeech.LANG_MISSING_DATA ||
                result == TextToSpeech.LANG_NOT_SUPPORTED
            ) {
                Log.w("VoiceService", "Tiếng Việt chưa được hỗ trợ")
            }
        } else {
            Log.w("VoiceService", "Khởi tạo TTS thất bại")
        }
    }

    fun speak(text: String) {
        if (!initialized || text.isBlank()) return
        tts.speak(
            text,
            TextToSpeech.QUEUE_FLUSH,
            null,
            "tts-${System.currentTimeMillis()}"
        )
    }

    fun shutdown() {
        tts.stop()
        tts.shutdown()
    }
}
