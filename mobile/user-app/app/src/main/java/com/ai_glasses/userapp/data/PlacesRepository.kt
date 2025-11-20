package com.ai_glasses.userapp.data

data class Place(
    val id: String,
    val name: String,
    val lat: Double,
    val lon: Double
)

/**
 * Repo đơn giản lưu list địa điểm quen trong bộ nhớ.
 * Sau này có thể thay bằng Room / sync backend.
 */
class PlacesRepository {

    private val inMemoryPlaces = mutableListOf<Place>()

    fun listPlaces(): List<Place> = inMemoryPlaces.toList()

    fun addPlace(place: Place) {
        inMemoryPlaces.add(place)
    }

    fun removePlace(id: String) {
        inMemoryPlaces.removeAll { it.id == id }
    }
}
