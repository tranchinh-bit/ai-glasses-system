package com.ai_glasses.familyapp

import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import okhttp3.*
import okio.ByteString
import java.util.concurrent.TimeUnit

data class AlertItem(
    val message: String,
    val level: String,
    val timestamp: Long,
)

class BackendClient(
    private val appScope: CoroutineScope,
    private val baseWsUrl: String,         // "wss://your-cloud/ws/family"
    private val deviceId: String,          // "glasses-001"
) {

    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()

    private val _alerts = MutableStateFlow<List<AlertItem>>(emptyList())
    val alerts = _alerts.asStateFlow()

    private val _connected = MutableStateFlow(false)
    val connected = _connected.asStateFlow()

    private var ws: WebSocket? = null

    fun start() {
        appScope.launch {
            connectLoop()
        }
    }

    private suspend fun connectLoop() {
        while (true) {
            try {
                val url = "$baseWsUrl?device_id=$deviceId"
                val request = Request.Builder().url(url).build()
                Log.i("BackendWS", "Connecting to $url")

                val listener = object : WebSocketListener() {
                    override fun onOpen(webSocket: WebSocket, response: Response) {
                        Log.i("BackendWS", "Connected")
                        _connected.value = true
                    }

                    override fun onMessage(webSocket: WebSocket, text: String) {
                        Log.d("BackendWS", "Message: $text")
                        // backend gửi JSON dạng:
                        // { "type":"alert","payload":{"message":"...","level":"CRITICAL","timestamp":...}}
                        handleJsonMessage(text)
                    }

                    override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                        Log.d("BackendWS", "Binary message: ${bytes.size}")
                    }

                    override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                        Log.w("BackendWS", "Closed: $code / $reason")
                        _connected.value = false
                    }

                    override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                        Log.e("BackendWS", "Failure: ${t.message}", t)
                        _connected.value = false
                    }
                }

                ws = client.newWebSocket(request, listener)

                while (_connected.value) {
                    kotlinx.coroutines.delay(2000)
                }
                ws?.close(1000, "reconnect")
                ws = null

                kotlinx.coroutines.delay(5000)

            } catch (e: Exception) {
                Log.e("BackendWS", "connectLoop error", e)
                _connected.value = false
                kotlinx.coroutines.delay(5000)
            }
        }
    }

    private fun handleJsonMessage(text: String) {
        // để đơn giản, parse rất thô (sau này dùng kotlinx.serialization)
        if (text.contains("\"type\":\"alert\"")) {
            val message = Regex("\"message\"\\s*:\\s*\"([^\"]+)\"").find(text)?.groupValues?.get(1) ?: "Alert"
            val level = Regex("\"level\"\\s*:\\s*\"([^\"]+)\"").find(text)?.groupValues?.get(1) ?: "INFO"
            val ts = Regex("\"timestamp\"\\s*:\\s*(\\d+)").find(text)?.groupValues?.get(1)?.toLongOrNull() ?: 0L

            val alert = AlertItem(message, level, ts)
            val current = _alerts.value.toMutableList()
            current.add(0, alert)
            _alerts.value = current.take(100) // giới hạn 100 alert gần nhất
        }
    }
}
