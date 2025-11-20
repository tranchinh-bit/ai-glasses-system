package com.ai_glasses.userapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun HomeScreen() {
    var isConnected by remember { mutableStateOf(false) }
    var lastMessage by remember { mutableStateOf("Chưa có thông báo nào.") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "AI Glasses – Người dùng",
            style = MaterialTheme.typography.titleLarge
        )

        Card(
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    "Trạng thái kết nối kính: " +
                            if (isConnected) "Đã kết nối" else "Chưa kết nối"
                )
                Text("Thông điệp gần nhất:")
                Text(lastMessage, style = MaterialTheme.typography.bodyMedium)
            }
        }

        Button(
            onClick = { /* TODO: điều hướng sang PlacesScreen */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Địa điểm quen")
        }

        Button(
            onClick = { /* TODO: điều hướng sang FacesScreen */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Khuôn mặt quen")
        }

        Button(
            onClick = { /* TODO: điều hướng sang SettingsScreen */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Cài đặt")
        }
    }
}
