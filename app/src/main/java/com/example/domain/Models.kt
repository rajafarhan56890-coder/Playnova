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
    val id: String = "",
    val title: String = "",
    val description: String = "",
    val category: String = "",
    val rewardPoints: Int = 0,
    val imageUrl: String? = null,
    val gameUrl: String? = null,
    val isActive: Boolean = true
)

data class Transaction(
    val id: String = "",
    val title: String = "",
    val amount: Long = 0,
    val isPositive: Boolean = true,
    val timestamp: Date = Date(),
    val type: String = "", // "reward", "withdrawal", "referral"
    val status: String = "completed"
)

data class Notification(
    val id: String = "",
    val title: String = "",
    val message: String = "",
    val timestamp: Date = Date(),
    val isRead: Boolean = false,
    val type: String = "" // "system", "reward", "announcement"
)

data class RewardTask(
    val id: String = "",
    val title: String = "",
    val description: String = "",
    val rewardAmount: Int = 0,
    val isCompleted: Boolean = false,
    val progress: Float = 0f // 0.0 to 1.0
)

data class WithdrawalRequest(
    val id: String = "",
    val userId: String = "",
    val amount: Long = 0,
    val paymentMethod: String = "", // EasyPaisa, JazzCash
    val accountDetails: String = "",
    val status: String = "pending", // pending, approved, rejected
    val timestamp: Date = Date()
)

data class Referral(
    val id: String = "",
    val referrerId: String = "",
    val referredId: String = "",
    val timestamp: Date = Date(),
    val bonusAwarded: Boolean = false
)
