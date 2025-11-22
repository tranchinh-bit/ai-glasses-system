package com.ai_glasses.userapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * Màn cài đặt: stub – sau có thể bind với UserPreferences.
 */
@Composable
fun SettingsScreen() {
    var wsUrl by remember { mutableStateOf("ws://192.168.1.10:9000/ws/mobile") }
    var backendUrl by remember { mutableStateOf("http://192.168.1.100:8000") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Cài đặt", style = MaterialTheme.typography.titleLarge)

        OutlinedTextField(
            value = wsUrl,
            onValueChange = { wsUrl = it },
            label = { Text("WS URL kính") },
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = backendUrl,
            onValueChange = { backendUrl = it },
            label = { Text("Backend URL") },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = { /* TODO: lưu vào UserPreferences */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Lưu cài đặt")
        }
    }
}
