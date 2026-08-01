package com.example.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.SetOptions
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import java.util.Date

sealed class DailyRewardState {
    object Loading : DailyRewardState()
    object Available : DailyRewardState()
    data class Claimed(val hoursLeft: Long) : DailyRewardState()
    data class Error(val message: String) : DailyRewardState()
}

class DailyRewardViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<DailyRewardState>(DailyRewardState.Loading)
    val uiState: StateFlow<DailyRewardState> = _uiState

    private val db: FirebaseFirestore? by lazy {
        try {
            FirebaseFirestore.getInstance()
        } catch (e: Exception) {
            null
        }
    }

    private val userId: String
        get() {
            return try {
                FirebaseAuth.getInstance().currentUser?.uid ?: "test_user_123"
            } catch (e: Exception) {
                "test_user_123"
            }
        }

    init {
        checkDailyReward()
    }

    fun checkDailyReward() {
        if (db == null) {
            _uiState.value = DailyRewardState.Error("Firebase not configured. Add google-services.json")
            return
        }
        viewModelScope.launch {
            try {
                _uiState.value = DailyRewardState.Loading
                val userRef = db!!.collection("users").document(userId)
                val snapshot = userRef.get().await()
                val lastClaimTimestamp = snapshot.getTimestamp("lastDailyReward")
                
                if (lastClaimTimestamp != null) {
                    val lastClaimDate = lastClaimTimestamp.toDate()
                    val currentDate = Date()
                    val diffInMillis = currentDate.time - lastClaimDate.time
                    val diffInHours = diffInMillis / (1000 * 60 * 60)
                    
                    if (diffInHours >= 24) {
                        _uiState.value = DailyRewardState.Available
                    } else {
                        val hoursLeft = 24 - diffInHours
                        _uiState.value = DailyRewardState.Claimed(hoursLeft)
                    }
                } else {
                    _uiState.value = DailyRewardState.Available
                }
            } catch (e: Exception) {
                _uiState.value = DailyRewardState.Error(e.message ?: "Unknown error")
            }
        }
    }

    fun claimReward() {
        if (db == null) return
        viewModelScope.launch {
            try {
                _uiState.value = DailyRewardState.Loading
                val userRef = db!!.collection("users").document(userId)
                db!!.runTransaction { transaction ->
                    val snapshot = transaction.get(userRef)
                    val currentBalance = snapshot.getLong("balance") ?: 0L
                    transaction.set(userRef, mapOf(
                        "balance" to currentBalance + 50,
                        "lastDailyReward" to FieldValue.serverTimestamp()
                    ), SetOptions.merge())
                }.await()
                
                _uiState.value = DailyRewardState.Claimed(24)
            } catch (e: Exception) {
                _uiState.value = DailyRewardState.Error(e.message ?: "Failed to claim")
            }
        }
    }
}
