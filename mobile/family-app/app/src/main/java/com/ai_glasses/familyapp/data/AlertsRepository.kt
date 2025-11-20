package com.ai_glasses.familyapp.data

data class Alert(
    val id: Long,
    val deviceId: String,
    val title: String,
    val message: String,
    val severity: String,
    val createdAt: String
)

/**
 * Repo cảnh báo – hiện tại lưu trong RAM, sau có thể bind REST.
 */
class AlertsRepository {
    private val inMemory = mutableListOf<Alert>()

    fun add(alert: Alert) {
        inMemory.add(0, alert)
    }

    fun list(): List<Alert> = inMemory.toList()
}
