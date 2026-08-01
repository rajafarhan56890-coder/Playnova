package com.example.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.Transaction
import com.example.domain.WithdrawalRequest
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await

data class AdminConfig(
    val conversionRateUSD: Double = 0.001, // 1 Nova = 0.001 USD
    val conversionRatePKR: Double = 0.28 // 1 Nova = 0.28 PKR
)

sealed class WalletState {
    object Loading : WalletState()
    data class Success(
        val balance: Long,
        val transactions: List<Transaction>,
        val config: AdminConfig
    ) : WalletState()
    data class Error(val message: String) : WalletState()
}

class WalletViewModel : ViewModel() {
    private val auth = try { FirebaseAuth.getInstance() } catch(e: Exception) { null }
    private val db = try { FirebaseFirestore.getInstance() } catch(e: Exception) { null }

    private val _walletState = MutableStateFlow<WalletState>(WalletState.Loading)
    val walletState: StateFlow<WalletState> = _walletState

    private val _withdrawState = MutableStateFlow<String?>(null)
    val withdrawState: StateFlow<String?> = _withdrawState
    
    init {
        fetchWalletData()
    }

    fun fetchWalletData() {
        val uid = auth?.currentUser?.uid
        if (uid == null) {
            // Mock fallback if user not logged in
            _walletState.value = WalletState.Success(
                balance = 0,
                transactions = emptyList(),
                config = AdminConfig()
            )
            return
        }

        viewModelScope.launch {
            try {
                _walletState.value = WalletState.Loading
                
                // Fetch user balance
                val userDoc = db?.collection("users")?.document(uid)?.get()?.await()
                val balance = userDoc?.getLong("balance") ?: 0L

                // Fetch transactions
                val transactionsSnapshot = db?.collection("users")?.document(uid)
                    ?.collection("transactions")
                    ?.orderBy("timestamp", Query.Direction.DESCENDING)
                    ?.limit(20)
                    ?.get()?.await()

                val transactions = transactionsSnapshot?.documents?.mapNotNull {
                    it.toObject(Transaction::class.java)?.copy(id = it.id)
                } ?: emptyList()

                // Fetch admin config
                val configDoc = db?.collection("admin")?.document("config")?.get()?.await()
                val config = configDoc?.toObject(AdminConfig::class.java) ?: AdminConfig()

                _walletState.value = WalletState.Success(balance, transactions, config)

            } catch (e: Exception) {
                _walletState.value = WalletState.Error(e.message ?: "Failed to load wallet")
            }
        }
    }

    fun requestWithdrawal(amount: Long, method: String, accountDetails: String) {
        val uid = auth?.currentUser?.uid ?: return
        
        viewModelScope.launch {
            try {
                val currentState = _walletState.value
                if (currentState is WalletState.Success) {
                    if (amount > currentState.balance) {
                        _withdrawState.value = "Error: Insufficient balance."
                        return@launch
                    }
                    if (amount <= 0) {
                        _withdrawState.value = "Error: Invalid amount."
                        return@launch
                    }

                    // We do NOT deduct balance here. It will be deducted when admin approves.
                    // Just create a withdrawal request.
                    
                    val requestRef = db?.collection("withdrawals")?.document()
                    val request = WithdrawalRequest(
                        id = requestRef?.id ?: "",
                        userId = uid,
                        amount = amount,
                        paymentMethod = method,
                        accountDetails = accountDetails
                    )

                    requestRef?.set(request)?.await()
                    
                    _withdrawState.value = "Withdrawal request submitted successfully!"
                    fetchWalletData() // Refresh data
                }
            } catch (e: Exception) {
                _withdrawState.value = "Error: ${e.message}"
            }
        }
    }

    fun clearWithdrawState() {
        _withdrawState.value = null
    }
}
