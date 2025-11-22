package com.ai_glasses.userapp

import android.util.Log
import com.ai_glasses.userapp.data.UserPreferences
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import okhttp3.*

import okio.ByteString
import java.util.concurrent.TimeUnit

enum class GlassesConnectionState {
    DISCONNECTED,
    CONNECTING,
    CONNECTED
}

/**
 * Quản lý WebSocket tới Pi (kính).
 * - Auto reconnect
 * - Cho phép gửi message JSON đơn giản
 */
class GlassesConnectionManager(
    private val appScope: CoroutineScope,
    private val userPreferences: UserPreferences,
) {

    private val client: OkHttpClient = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS) // WebSocket
        .build()

    private var webSocket: WebSocket? = null

    private val _state = MutableStateFlow(GlassesConnectionState.DISCONNECTED)
    val state = _state.asStateFlow()

    fun start() {
        appScope.launch {
            connectLoop()
        }
    }

    fun stop() {
        webSocket?.close(1000, "Manual close")
        webSocket = null
        _state.value = GlassesConnectionState.DISCONNECTED
    }

    private suspend fun connectLoop() {
        while (true) {
            try {
                if (_state.value != GlassesConnectionState.DISCONNECTED) {
                    // đã có connection / đang connect
                    kotlinx.coroutines.delay(5000)
                    continue
                }

                val wsUrl = userPreferences.getWsUrl()
                if (wsUrl.isBlank()) {
                    Log.w("GlassesWS", "WS URL is blank, skip connecting")
                    kotlinx.coroutines.delay(5000)
                    continue
                }

                _state.value = GlassesConnectionState.CONNECTING

                val request = Request.Builder()
                    .url(wsUrl)
                    .build()

                val listener = object : WebSocketListener() {
                    override fun onOpen(webSocket: WebSocket, response: Response) {
                        Log.i("GlassesWS", "WebSocket opened")
                        _state.value = GlassesConnectionState.CONNECTED
                        // gửi handshake đơn giản
                        webSocket.send("""{"type":"hello","client":"user_app"}""")
                    }

                    override fun onMessage(webSocket: WebSocket, text: String) {
                        Log.d("GlassesWS", "Message: $text")
                        // TODO: parse type = heartbeat / config / alert...
                    }

                    override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                        // Nếu sau này dùng protobuf binary, xử lý tại đây
                        Log.d("GlassesWS", "Binary message: ${bytes.size} bytes")
                    }

                    override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                        Log.w("GlassesWS", "Closed: $code / $reason")
                        _state.value = GlassesConnectionState.DISCONNECTED
                    }

                    override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                        Log.e("GlassesWS", "Failure: ${t.message}", t)
                        _state.value = GlassesConnectionState.DISCONNECTED
                    }
                }

                webSocket = client.newWebSocket(request, listener)

                // Chờ trong khi CONNECTED
                while (_state.value == GlassesConnectionState.CONNECTED) {
                    kotlinx.coroutines.delay(1000)
                }

                // nếu ra khỏi vòng CONNECTED, close socket
                webSocket?.close(1000, "Reconnect loop")
                webSocket = null

                // delay trước khi thử lại
                kotlinx.coroutines.delay(5000)

            } catch (e: Exception) {
                Log.e("GlassesWS", "connectLoop error", e)
                _state.value = GlassesConnectionState.DISCONNECTED
                kotlinx.coroutines.delay(5000)
            }
        }
    }

    fun sendJson(json: String) {
        webSocket?.send(json)
    }
}
