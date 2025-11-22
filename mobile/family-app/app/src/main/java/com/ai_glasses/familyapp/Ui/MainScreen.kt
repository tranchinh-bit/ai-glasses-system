package com.ai_glasses.familyapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalContext
import com.ai_glasses.familyapp.BackendClient
import com.ai_glasses.familyapp.data.DeviceSelectionRepository
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers

@Composable
fun MainScreen() {
    val ctx = LocalContext.current
    val scope = remember { CoroutineScope(Dispatchers.IO) }

    val deviceRepo = remember { DeviceSelectionRepository() }
    val devices = deviceRepo.getDevices()
    var selectedDeviceId by remember { mutableStateOf(devices.firstOrNull()?.deviceId ?: "") }

    val backendClient = remember(selectedDeviceId) {
        BackendClient(
            appScope = scope,
            baseWsUrl = "wss://your-cloud-backend/ws/family",
            deviceId = selectedDeviceId,
        ).apply { start() }
    }

    val connected by backendClient.connected.collectAsState()
    val alerts by backendClient.alerts.collectAsState()

    var tabIndex by remember { mutableStateOf(0) }
    val tabs = listOf("Map", "Alerts", "Settings")

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text("AI Glasses – Family") }
        )

        Row(Modifier.padding(8.dp)) {
            Text("Thiết bị: ")
            Spacer(Modifier.width(8.dp))
            DropdownMenuDeviceSelector(
                devices = devices.map { it.deviceId to it.name },
                selectedId = selectedDeviceId,
                onSelected = { selectedDeviceId = it },
            )
        }

        Text(
            text = "Trạng thái kết nối: ${if (connected) "ONLINE" else "OFFLINE"}",
            modifier = Modifier.padding(horizontal = 16.dp)
        )

        TabRow(selectedTabIndex = tabIndex) {
            tabs.forEachIndexed { i, title ->
                Tab(
                    selected = tabIndex == i,
                    onClick = { tabIndex = i },
                    text = { Text(title) }
                )
            }
        }

        when (tabIndex) {
            0 -> MapScreen()
            1 -> AlertsScreen(alerts = alerts)
            2 -> SettingsScreen()
        }
    }
}

@Composable
private fun DropdownMenuDeviceSelector(
    devices: List<Pair<String, String>>,
    selectedId: String,
    onSelected: (String) -> Unit,
) {
    var expanded by remember { mutableStateOf(false) }
    val currentName = devices.find { it.first == selectedId }?.second ?: "None"

    Box {
        OutlinedButton(onClick = { expanded = true }) {
            Text(currentName)
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            devices.forEach { (id, name) ->
                DropdownMenuItem(
                    text = { Text(name) },
                    onClick = {
                        onSelected(id)
                        expanded = false
                    }
                )
            }
        }
    }
}
