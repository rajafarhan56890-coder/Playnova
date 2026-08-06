with open('app/src/main/java/com/example/ui/viewmodels/AuthViewModel.kt', 'r') as f:
    content = f.read()

import re

old_add_balance = """    fun addBalance(amount: Long, title: String) {
        val uid = auth?.currentUser?.uid ?: return
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
    }"""

new_add_balance = """    fun addBalance(amount: Long, title: String) {
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
    }"""

content = content.replace(old_add_balance, new_add_balance)

with open('app/src/main/java/com/example/ui/viewmodels/AuthViewModel.kt', 'w') as f:
    f.write(content)
