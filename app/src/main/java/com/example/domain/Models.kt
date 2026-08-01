package com.example.domain

import java.util.Date

data class UserProfile(
    val uid: String = "",
    val email: String = "",
    val username: String = "",
    val balance: Long = 0,
    val level: Int = 1,
    val rank: String = "Bronze",
    val referralCode: String = "",
    val profileImageUrl: String? = null
)

data class Game(
    val id: String,
    val title: String,
    val description: String,
    val category: String,
    val rewardPoints: Int,
    val imageUrl: String? = null
)

data class Transaction(
    val id: String,
    val title: String,
    val amount: Long,
    val isPositive: Boolean,
    val timestamp: Date,
    val type: String // "reward", "withdrawal", "referral"
)

data class Notification(
    val id: String,
    val title: String,
    val message: String,
    val timestamp: Date,
    val isRead: Boolean,
    val type: String // "system", "reward", "announcement"
)

data class RewardTask(
    val id: String,
    val title: String,
    val description: String,
    val rewardAmount: Int,
    val isCompleted: Boolean,
    val progress: Float = 0f // 0.0 to 1.0
)
