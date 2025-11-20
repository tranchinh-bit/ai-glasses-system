package com.ai_glasses.userapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.ai_glasses.userapp.data.Place
import com.ai_glasses.userapp.data.PlacesRepository

@Composable
fun PlacesScreen(
    repo: PlacesRepository = PlacesRepository()
) {
    var places by remember { mutableStateOf(repo.listPlaces()) }
    var name by remember { mutableStateOf("") }
    var lat by remember { mutableStateOf("") }
    var lon by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Địa điểm quen", style = MaterialTheme.typography.titleLarge)

        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Tên địa điểm") },
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = lat,
            onValueChange = { lat = it },
            label = { Text("Vĩ độ (lat)") },
            modifier = Modifier.fillMaxWidth()
        )
        OutlinedTextField(
            value = lon,
            onValueChange = { lon = it },
            label = { Text("Kinh độ (lon)") },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = {
                val dLat = lat.toDoubleOrNull()
                val dLon = lon.toDoubleOrNull()
                if (!name.isBlank() && dLat != null && dLon != null) {
                    val p = Place(
                        id = "place-${System.currentTimeMillis()}",
                        name = name.trim(),
                        lat = dLat,
                        lon = dLon
                    )
                    repo.addPlace(p)
                    places = repo.listPlaces()
                    name = ""
                    lat = ""
                    lon = ""
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Thêm địa điểm")
        }

        Divider()

        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(places) { p ->
                Card {
                    Column(Modifier.padding(12.dp)) {
                        Text(p.name, style = MaterialTheme.typography.titleMedium)
                        Text("Lat: ${p.lat}, Lon: ${p.lon}")
                    }
                }
            }
        }
    }
}
