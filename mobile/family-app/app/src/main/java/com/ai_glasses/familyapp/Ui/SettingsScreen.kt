package com.ai_glasses.familyapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun SettingsScreen() {
    var wsUrl by remember { mutableStateOf("ws://192.168.1.100:8000/ws/family") }

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
            label = { Text("Backend WS URL") },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = { /* TODO: lưu config vào DataStore / SharedPreferences */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Lưu")
        }
    }
}
