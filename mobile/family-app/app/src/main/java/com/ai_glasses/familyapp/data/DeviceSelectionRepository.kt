package com.ai_glasses.familyapp.data

data class Device(
    val deviceId: String,
    val name: String,
)

class DeviceSelectionRepository {
    // tạm thời hard-code 1 thiết bị, sau này load từ backend
    private val devices = listOf(
        Device("glasses-001", "Kính của Ba"),
    )

    fun getDevices(): List<Device> = devices
}
