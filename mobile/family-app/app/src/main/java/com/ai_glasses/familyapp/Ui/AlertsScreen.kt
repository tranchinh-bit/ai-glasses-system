package com.ai_glasses.familyapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.ai_glasses.familyapp.AlertItem
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun AlertsScreen(alerts: List<AlertItem>) {
    val df = remember { SimpleDateFormat("HH:mm:ss dd/MM", Locale.getDefault()) }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        items(alerts) { alert ->
            Card {
                Column(Modifier.padding(8.dp)) {
                    Text(text = alert.message)
                    Text(text = "Level: ${alert.level}")
                    Text(text = df.format(Date(alert.timestamp)))
                }
            }
        }
    }
}
