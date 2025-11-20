package com.ai_glasses.familyapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/**
 * Stub hiển thị bản đồ – sau này có thể tích hợp Google Maps SDK.
 */
@Composable
fun MapScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Vị trí hiện tại của kính", style = MaterialTheme.typography.titleLarge)
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(300.dp)
        ) {
            Box(Modifier.fillMaxSize()) {
                Text(
                    "Map placeholder\n(Sau này gắn Google Maps / Mapbox)",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}
