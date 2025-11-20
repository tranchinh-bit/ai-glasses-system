package com.ai_glasses.userapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

data class KnownFace(
    val id: String,
    val name: String
)

/**
 * Stub quản lý khuôn mặt quen. Sau này có thể sync với Pi-core / backend.
 */
@Composable
fun FacesScreen() {
    var faces by remember {
        mutableStateOf(
            listOf(
                KnownFace("1", "Ba"),
                KnownFace("2", "Mẹ")
            )
        )
    }
    var newName by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Khuôn mặt quen", style = MaterialTheme.typography.titleLarge)

        OutlinedTextField(
            value = newName,
            onValueChange = { newName = it },
            label = { Text("Tên người mới") },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = {
                if (newName.isNotBlank()) {
                    faces = faces + KnownFace(
                        id = "face-${System.currentTimeMillis()}",
                        name = newName.trim()
                    )
                    newName = ""
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Thêm khuôn mặt")
        }

        Divider()

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(faces) { f ->
                Card {
                    Column(Modifier.padding(12.dp)) {
                        Text(f.name, style = MaterialTheme.typography.titleMedium)
                        Text("ID: ${f.id}", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
}
