package com.ai_glasses.familyapp

import android.util.Log
import com.google.gson.Gson
import okhttp3.*
import java.util.concurrent.CopyOnWriteArrayList

/**
 * Nhận alert realtime từ backend qua WebSocket /ws/family.
 */
class BackendClient(
    private val wsUrl: String
) {
    private val client = OkHttpClient()
    private var ws: WebSocket? = null
    private val listeners = CopyOnWriteArrayList<(String) -> Unit>()
    private val gson = Gson()

    fun connect() {
        val req = Request.Builder().url(wsUrl).build()
        ws = client.newWebSocket(
            req,
            object : WebSocketListener() {
                override fun onOpen(webSocket: WebSocket, response: Response) {
                    Log.d("BackendClient", "WS connected")
                }

                override fun onMessage(webSocket: WebSocket, text: String) {
                    listeners.forEach { it(text) }
                }

                override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                    Log.w("BackendClient", "WS error: ${t.message}")
                }

                override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                    Log.d("BackendClient", "WS closed: $code $reason")
                }
            }
        )
    }

    fun addListener(listener: (String) -> Unit) {
        listeners.add(listener)
    }

    fun close() {
        ws?.close(1000, "closed")
    }
}
