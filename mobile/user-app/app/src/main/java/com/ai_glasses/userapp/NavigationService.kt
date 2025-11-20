package com.ai_glasses.userapp

import android.util.Log
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody

/**
 * Gọi REST tới backend để lấy hướng dẫn điều hướng.
 */
class NavigationService(
    private val backendBaseUrl: String
) {
    private val client = OkHttpClient()
    private val gson = Gson()

    suspend fun requestNextInstruction(location: Map<String, Any>): Map<String, Any> =
        withContext(Dispatchers.IO) {
            val url = "$backendBaseUrl/api/v1/nav/next"
            val json = gson.toJson(location)
            val body = RequestBody.create(
                "application/json".toMediaType(),
                json
            )
            val req = Request.Builder()
                .url(url)
                .post(body)
                .build()

            return@withContext try {
                client.newCall(req).execute().use { resp ->
                    if (!resp.isSuccessful) {
                        Log.w("NavigationService", "HTTP ${resp.code}")
                        emptyMap()
                    } else {
                        val text = resp.body?.string().orEmpty()
                        if (text.isBlank()) emptyMap()
                        else gson.fromJson(text, Map::class.java) as Map<String, Any>
                    }
                }
            } catch (e: Exception) {
                Log.w("NavigationService", "Error: ${e.message}")
                emptyMap()
            }
        }
}
