package com.ai_glasses.familyapp.data

import com.ai_glasses.familyapp.AlertItem
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow

class AlertsRepository {
    private val _alerts = MutableStateFlow<List<AlertItem>>(emptyList())
    val alerts = _alerts.asStateFlow()

    fun updateFromBackend(list: List<AlertItem>) {
        _alerts.value = list
    }
}
