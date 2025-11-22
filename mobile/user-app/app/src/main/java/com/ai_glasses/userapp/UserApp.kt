package com.ai_glasses.userapp

import android.app.Application
import com.ai_glasses.userapp.data.UserPreferences
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob

class UserApp : Application() {

    lateinit var appScope: CoroutineScope
        private set

    lateinit var userPreferences: UserPreferences
        private set

    override fun onCreate() {
        super.onCreate()
        appScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
        userPreferences = UserPreferences(this)
    }
}
