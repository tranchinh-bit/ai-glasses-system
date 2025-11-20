package com.ai_glasses.userapp

import android.app.Application
import com.ai_glasses.userapp.data.UserPreferences
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.SupervisorJob

class UserApp : Application() {

    val applicationScope = CoroutineScope(SupervisorJob())
    lateinit var userPreferences: UserPreferences

    override fun onCreate() {
        super.onCreate()
        userPreferences = UserPreferences(this)
    }
}
