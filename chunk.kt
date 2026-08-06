    fun signUp(email: String, pass: String, referralCode: String? = null) {
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
                    username = email.substringBefore("@"),
                    balance = signupBonus, // Welcome bonus if referred
