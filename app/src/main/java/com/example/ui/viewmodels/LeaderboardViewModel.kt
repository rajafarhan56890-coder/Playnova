package com.example.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.UserProfile
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

sealed class LeaderboardState {
    object Loading : LeaderboardState()
    data class Success(val users: List<UserProfile>) : LeaderboardState()
    data class Error(val message: String) : LeaderboardState()
}

class LeaderboardViewModel : ViewModel() {
    private val db = try { FirebaseFirestore.getInstance() } catch(e: Exception) { null }

    private val _uiState = MutableStateFlow<LeaderboardState>(LeaderboardState.Loading)
    val uiState: StateFlow<LeaderboardState> = _uiState

    init {
        fetchLeaderboard()
    }

    fun fetchLeaderboard() {
        viewModelScope.launch {
            _uiState.value = LeaderboardState.Loading
            try {
                if (db == null) {
                    // Mock data if no Firebase
                    val mockUsers = (1..20).map { i ->
                        UserProfile(
                            uid = "user$i",
                            username = "Player $i",
                            balance = (2000 - i * 50).toLong(),
                            level = (20 - i + 1),
                            rank = if (i < 4) "Diamond" else "Gold"
                        )
                    }
                    _uiState.value = LeaderboardState.Success(mockUsers)
                    return@launch
                }

                val snapshot = db.collection("users")
                    .orderBy("balance", Query.Direction.DESCENDING)
                    .limit(20)
                    .get()
                    .await()

                val users = snapshot.documents.mapNotNull { doc ->
                    doc.toObject(UserProfile::class.java)
                }

                _uiState.value = LeaderboardState.Success(users)
            } catch (e: Exception) {
                _uiState.value = LeaderboardState.Error(e.message ?: "Failed to fetch leaderboard")
            }
        }
    }
}
