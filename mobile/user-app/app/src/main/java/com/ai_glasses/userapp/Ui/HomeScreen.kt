package com.ai_glasses.userapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonRow
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.ai_glasses.userapp.GlassesConnectionManager
import com.ai_glasses.userapp.GlassesConnectionState
import com.ai_glasses.userapp.UserApp
import kotlinx.coroutines.launch

@Composable
fun HomeScreen() {
    val context = LocalContext.current
    val app = context.applicationContext as UserApp
    val scope = rememberCoroutineScope()

    // Khởi tạo connection manager 1 lần
    val connManager = remember {
        GlassesConnectionManager(app.appScope, app.userPreferences).apply { start() }
    }

    val connState by connManager.state.collectAsState()

    var wsUrlText by remember { mutableStateOf("ws://192.168.43.1:8765/api/v1/glasses") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(text = "AI Glasses – User App")

        Text(text = "Trạng thái kết nối: $connState")

        OutlinedTextField(
            value = wsUrlText,
            onValueChange = { wsUrlText = it },
            label = { Text("WS URL tới Pi") },
            modifier = Modifier.fillMaxWidth()
        )

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = {
                scope.launch { app.userPreferences.setWsUrl(wsUrlText) }
            }) {
                Text("Lưu WS URL")
            }
            OutlinedButton(onClick = { connManager.stop() }) {
                Text("Ngắt kết nối")
            }
        }

        Spacer(Modifier.height(32.dp))

        Text("Chế độ Offload:")
        var selectedMode by remember { mutableStateOf("AUTO") }

        SegmentedButtonRow {
            listOf("AUTO", "LOCAL", "PHONE").forEach { mode ->
                SegmentedButton(
                    selected = selectedMode == mode,
                    onClick = {
                        selectedMode = mode
                        scope.launch {
                            app.userPreferences.setOffloadMode(mode)
                            connManager.sendJson("""{"type":"config_update","offload_mode":"$mode"}""")
                        }
                    },
                    label = { Text(mode) },
                )
            }
        }

        Spacer(Modifier.height(16.dp))

        Button(onClick = {
            connManager.sendJson("""{"type":"sos","reason":"button"}""")
        }) {
            Text("Gửi SOS")
        }
    }
}
