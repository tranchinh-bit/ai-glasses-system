package com.ai_glasses.familyapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

@Composable
fun SettingsScreen() {
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("Settings (khung)")
        Text("- Cloud URL")
        Text("- Ngôn ngữ")
        Text("- Thông báo")
    }
}
