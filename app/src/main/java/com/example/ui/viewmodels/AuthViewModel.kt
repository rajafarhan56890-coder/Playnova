package com.example.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.UserProfile
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.FieldValue
import com.example.domain.Transaction
import com.example.domain.Referral
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
    
    fun signUp(email: String, pass: String, username: String, referralCode: String? = null) {
        if (auth == null) {
            checkCurrentUser() // mock success
            return
        }
        viewModelScope.launch {
            _authState.value = AuthState.Loading
            try {
                var referrerId: String? = null
                var signupBonus: Long = 0L

                if (!referralCode.isNullOrEmpty()) {
                    val query = db?.collection("users")?.whereEqualTo("referralCode", referralCode)?.limit(1)?.get()?.await()
                    if (query != null && !query.isEmpty) {
                        referrerId = query.documents[0].id
                        signupBonus = 200L // New user gets 200 Nova bonus
                    }
                }

                val result = auth.createUserWithEmailAndPassword(email, pass).await()
                val uid = result.user!!.uid
                val newUser = UserProfile(
                    uid = uid,
                    email = email,
                    username = username,
                    balance = signupBonus, // Welcome bonus if referred
                    level = 1,
                    rank = "Bronze",
                    referralCode = generateReferralCode()
                )

                db?.runBatch { batch ->
                    val userRef = db.collection("users").document(uid)
                    batch.set(userRef, newUser)
                    
                    if (signupBonus > 0L) {
                        val transactionRef = db.collection("users").document(uid).collection("transactions").document()
                        batch.set(transactionRef, Transaction(
                            id = transactionRef.id,
                            title = "Sign Up Bonus",
                            amount = signupBonus,
                            isPositive = true,
                            type = "reward",
                            status = "completed"
                        ))
                    }

                    if (referrerId != null) {
                        val referrerRef = db.collection("users").document(referrerId)
                        batch.update(referrerRef, "balance", FieldValue.increment(500L))

                        val referrerTxRef = db.collection("users").document(referrerId).collection("transactions").document()
                        batch.set(referrerTxRef, Transaction(
                            id = referrerTxRef.id,
                            title = "Referral Bonus",
                            amount = 500L,
                            isPositive = true,
                            type = "referral",
                            status = "completed"
                        ))

                        val referralDocRef = db.collection("referrals").document()
                        batch.set(referralDocRef, Referral(
                            id = referralDocRef.id,
                            referrerId = referrerId,
                            referredId = uid,
                            bonusAwarded = true
                        ))
                    }
                }?.await()
                
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

    fun updateProfile(username: String, profileImageUrl: String?) {
        val uid = auth?.currentUser?.uid ?: return
        viewModelScope.launch {
            try {
                val updates = mutableMapOf<String, Any>(
                    "username" to username
                )
                if (profileImageUrl != null) {
                    updates["profileImageUrl"] = profileImageUrl
                }
                db?.collection("users")?.document(uid)?.update(updates)?.await()
            } catch (e: Exception) {
                // Handle error if needed
            }
        }
    }

    private fun generateReferralCode(): String {
        return "NOVA-" + UUID.randomUUID().toString().substring(0, 5).uppercase()
    }
    fun addBalance(amount: Long, title: String) {
        val uid = auth?.currentUser?.uid
        if (uid == null) {
            val current = _authState.value
            if (current is AuthState.Success) {
                _authState.value = AuthState.Success(current.user.copy(balance = current.user.balance + amount))
            }
            return
        }
        
        viewModelScope.launch {
            try {
                db?.runBatch { batch ->
                    val userRef = db.collection("users").document(uid)
                    batch.update(userRef, "balance", FieldValue.increment(amount))
                    val txRef = db.collection("users").document(uid).collection("transactions").document()
                    batch.set(txRef, Transaction(
                        id = txRef.id,
                        title = title,
                        amount = amount,
                        isPositive = true,
                        type = "reward",
                        status = "completed"
                    ))
                }?.await()
            } catch(e: Exception) {
            }
        }
    }

}
