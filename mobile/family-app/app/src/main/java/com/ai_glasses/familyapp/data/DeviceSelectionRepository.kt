package com.ai_glasses.familyapp.data

data class Device(
    val id: String,
    val name: String
)

/**
 * Danh sách thiết bị theo dõi – stub, sau có thể lấy từ backend.
 */
class DeviceSelectionRepository {
    private val devices = listOf(
        Device("pi-glasses-001", "Kính của Ba"),
        Device("pi-glasses-002", "Kính của Mẹ")
    )

    fun listDevices(): List<Device> = devices
}
