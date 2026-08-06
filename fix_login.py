import os

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()

old_signup = """        AnimatedVisibility(visible = isSignUp) {
            Column {
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = referralCode,
                    onValueChange = { referralCode = it },
                    label = { Text("Referral Code (Optional)") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
            }
        }"""

new_signup = """        AnimatedVisibility(visible = isSignUp) {
            Column {
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = username,
                    onValueChange = { username = it },
                    label = { Text("Username") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = confirmPassword,
                    onValueChange = { confirmPassword = it },
                    label = { Text("Confirm Password") },
                    visualTransformation = PasswordVisualTransformation(),
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    singleLine = true
                )
                Spacer(modifier = Modifier.height(16.dp))
                OutlinedTextField(
                    value = referralCode,
                    onValueChange = { referralCode = it },
                    label = { Text("Referral Code (Optional)") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
            }
        }"""

content = content.replace(old_signup, new_signup)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)

