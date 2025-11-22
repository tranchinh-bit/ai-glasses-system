package com.ai_glasses.userapp.data

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore("user_prefs")

class UserPreferences(private val context: Context) {

    companion object {
        private val KEY_WS_URL = stringPreferencesKey("ws_url")
        private val KEY_OFFLOAD_MODE = stringPreferencesKey("offload_mode")
    }

    suspend fun setWsUrl(url: String) {
        context.dataStore.edit { prefs ->
            prefs[KEY_WS_URL] = url
        }
    }

    suspend fun setOffloadMode(mode: String) {
        context.dataStore.edit { prefs ->
            prefs[KEY_OFFLOAD_MODE] = mode
        }
    }

    suspend fun getWsUrlFlow() =
        context.dataStore.data.map { prefs -> prefs[KEY_WS_URL] ?: "ws://192.168.43.1:8765/api/v1/glasses" }

    suspend fun getOffloadModeFlow() =
        context.dataStore.data.map { prefs -> prefs[KEY_OFFLOAD_MODE] ?: "AUTO" }

    // Hàm sync nhanh cho WS manager
    suspend fun getWsUrl(): String = getWsUrlFlow().first()
}
