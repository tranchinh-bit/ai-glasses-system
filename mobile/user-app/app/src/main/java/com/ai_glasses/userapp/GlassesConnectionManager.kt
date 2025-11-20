package com.ai_glasses.userapp

import android.util.Log
import com.google.gson.Gson
import okhttp3.*

/**
 * Kết nối WebSocket tới Pi-core hoặc backend đóng vai trò IO Hub.
 * Dùng để nhận hazard / status realtime và gửi lệnh đơn giản.
 */
class GlassesConnectionManager(
    private val url: String,
    private val onMessage: (String) -> Unit,
    private val onStateChange: (Boolean) -> Unit
) {
    private val client = OkHttpClient()
    private var webSocket: WebSocket? = null
    private val gson = Gson()

    fun connect() {
        val request = Request.Builder().url(url).build()
        webSocket = client.newWebSocket(
            request,
            object : WebSocketListener() {
                override fun onOpen(webSocket: WebSocket, response: Response) {
                    Log.d("GlassesConnection", "WebSocket opened")
                    onStateChange(true)
                }

                override fun onMessage(webSocket: WebSocket, text: String) {
                    onMessage(text)
                }

                override fun onFailure(
                    webSocket: WebSocket,
                    t: Throwable,
                    response: Response?
                ) {
                    Log.w("GlassesConnection", "WebSocket failure: ${t.message}")
                    onStateChange(false)
                }

                override fun onClosed(
                    webSocket: WebSocket,
                    code: Int,
                    reason: String
                ) {
                    Log.d("GlassesConnection", "WebSocket closed: $code $reason")
                    onStateChange(false)
                }
            }
        )
    }

    fun send(obj: Any) {
        val json = gson.toJson(obj)
        webSocket?.send(json)
    }

    fun close() {
        webSocket?.close(1000, "User closed")
    }
}
