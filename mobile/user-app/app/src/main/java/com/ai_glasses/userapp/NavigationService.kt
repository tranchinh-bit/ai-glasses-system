package com.ai_glasses.userapp

import android.util.Log

class NavigationService {

    fun startNavigationToPlace(placeId: String) {
        Log.d("NavigationService", "startNavigationToPlace: $placeId")
        // TODO: gửi NavCommand tới Pi / dùng Maps Intent
    }

    fun stopNavigation() {
        Log.d("NavigationService", "stopNavigation")
    }
}
