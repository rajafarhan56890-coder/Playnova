package com.example.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.UserProfile
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import java.util.UUID

sealed class AuthState {
    object Idle : AuthState()
    object Loading : AuthState()
    data class Success(val user: UserProfile) : AuthState()
    data class Error(val message: String) : AuthState()
}

class AuthViewModel : ViewModel() {
    private val auth = try { FirebaseAuth.getInstance() } catch(e: Exception) { null }
    private val db = try { FirebaseFirestore.getInstance() } catch(e: Exception) { null }

    private val _authState = MutableStateFlow<AuthState>(AuthState.Idle)
    val authState: StateFlow<AuthState> = _authState

    init {
        checkCurrentUser()
    }

    private fun checkCurrentUser() {
        // Fallback for AI Studio without Firebase configured
        if (auth == null) {
            val mockUser = UserProfile(
                uid = "mock123",
                email = "playerone@example.com",
                username = "PlayerOne",
                balance = 0,
                level = 12,
                rank = "Gold Elite",
                referralCode = "NOVA-X79B"
            )
            _authState.value = AuthState.Success(mockUser)
            return
        }

        val currentUser = auth.currentUser
        if (currentUser != null) {
            fetchUserProfile(currentUser.uid)
        }
    }

    fun login(email: String, pass: String) {
        if (auth == null) {
            checkCurrentUser() // mock success
            return
        }
        viewModelScope.launch {
            _authState.value = AuthState.Loading
            try {
                auth.signInWithEmailAndPassword(email, pass).await()
                fetchUserProfile(auth.currentUser!!.uid)
            } catch (e: Exception) {
                _authState.value = AuthState.Error(e.message ?: "Login failed")
            }
        }
    }

    fun signUp(email: String, pass: String) {
        if (auth == null) {
            checkCurrentUser() // mock success
            return
        }
        viewModelScope.launch {
            _authState.value = AuthState.Loading
            try {
                val result = auth.createUserWithEmailAndPassword(email, pass).await()
                val uid = result.user!!.uid
                val newUser = UserProfile(
                    uid = uid,
                    email = email,
                    username = email.substringBefore("@"),
                    balance = 0, // No welcome bonus
                    level = 1,
                    rank = "Bronze",
                    referralCode = generateReferralCode()
                )
                db?.collection("users")?.document(uid)?.set(newUser)?.await()
                _authState.value = AuthState.Success(newUser)
            } catch (e: Exception) {
                _authState.value = AuthState.Error(e.message ?: "Sign up failed")
            }
        }
    }

    fun logout() {
        auth?.signOut()
        _authState.value = AuthState.Idle
    }

    private fun fetchUserProfile(uid: String) {
        try {
            db?.collection("users")?.document(uid)?.addSnapshotListener { snapshot, error ->
                if (error != null) {
                    _authState.value = AuthState.Error(error.message ?: "Failed to fetch profile")
                    return@addSnapshotListener
                }
                val user = snapshot?.toObject(UserProfile::class.java)
                if (user != null) {
                    _authState.value = AuthState.Success(user)
                } else {
                    _authState.value = AuthState.Error("User profile not found")
                }
            }
        } catch (e: Exception) {
            _authState.value = AuthState.Error(e.message ?: "Failed to fetch profile")
        }
    }

    private fun generateReferralCode(): String {
        return "NOVA-" + UUID.randomUUID().toString().substring(0, 5).uppercase()
    }
}
