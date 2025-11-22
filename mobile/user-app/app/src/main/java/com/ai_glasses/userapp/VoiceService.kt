package com.ai_glasses.userapp

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import java.util.Locale

class VoiceService(context: Context) : TextToSpeech.OnInitListener {

    private var tts: TextToSpeech? = null
    private var isReady = false

    init {
        tts = TextToSpeech(context.applicationContext, this)
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            tts?.language = Locale("vi", "VN")
            isReady = true
        } else {
            Log.e("VoiceService", "TTS init failed: $status")
        }
    }

    fun speak(text: String) {
        if (!isReady) return
        tts?.speak(text, TextToSpeech.QUEUE_ADD, null, "tts-${System.currentTimeMillis()}")
    }

    fun shutdown() {
        tts?.shutdown()
        tts = null
    }
}
