package com.ai_glasses.userapp.data

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore("user_prefs")

class UserPreferences(private val context: Context) {

    private object Keys {
        val DEVICE_ID = stringPreferencesKey("device_id")
        val BACKEND_URL = stringPreferencesKey("backend_url")
        val GLASSES_WS_URL = stringPreferencesKey("glasses_ws_url")
    }

    val deviceId: Flow<String> = context.dataStore.data.map {
        it[Keys.DEVICE_ID] ?: "user-phone-001"
    }

    val backendUrl: Flow<String> = context.dataStore.data.map {
        it[Keys.BACKEND_URL] ?: "http://192.168.1.100:8000"
    }

    val glassesWsUrl: Flow<String> = context.dataStore.data.map {
        it[Keys.GLASSES_WS_URL] ?: "ws://192.168.1.10:9000/ws/mobile"
    }

    suspend fun setDeviceId(id: String) {
        context.dataStore.edit {
            it[Keys.DEVICE_ID] = id
        }
    }

    suspend fun setBackendUrl(url: String) {
        context.dataStore.edit {
            it[Keys.BACKEND_URL] = url
        }
    }

    suspend fun setGlassesWsUrl(url: String) {
        context.dataStore.edit {
            it[Keys.GLASSES_WS_URL] = url
        }
    }
}
