package com.ai_glasses.userapp.data

data class Place(
    val id: String,
    val name: String,
    val lat: Double,
    val lon: Double,
)

class PlacesRepository {

    // Tạm thời giữ in-memory, sau này có thể dùng Room
    private val places = mutableListOf<Place>()

    fun getAll(): List<Place> = places.toList()

    fun add(place: Place) {
        places += place
    }

    fun remove(id: String) {
        places.removeAll { it.id == id }
    }
}
