package com.ai_glasses.familyapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.ai_glasses.familyapp.data.Alert

@Composable
fun AlertsScreen() {
    // Stub: trong thực tế sẽ dùng BackendClient + AlertsRepository
    val alerts = remember {
        mutableStateListOf(
            Alert(
                id = 1,
                deviceId = "pi-glasses-001",
                title = "Cảnh báo vật cản phía trước",
                message = "Có vật cản cách khoảng 1.5m phía trước.",
                severity = "SEVERITY_WARNING",
                createdAt = "2025-11-21T10:00:00"
            )
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Cảnh báo từ kính", style = MaterialTheme.typography.titleLarge)

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(alerts) { alert ->
                Card {
                    Column(Modifier.padding(12.dp)) {
                        Text(alert.title, style = MaterialTheme.typography.titleMedium)
                        Text(alert.message, style = MaterialTheme.typography.bodyMedium)
                        Text(
                            "Thiết bị: ${alert.deviceId} • ${alert.createdAt}",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }
            }
        }
    }
}
