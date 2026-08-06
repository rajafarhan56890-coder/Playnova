import os

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("val uiState by authViewModel.uiState.collectAsState()", "val authState by authViewModel.authState.collectAsState()")
content = content.replace("val user = uiState.user", "val user = (authState as? com.example.ui.viewmodels.AuthState.Success)?.user")
content = content.replace("import com.example.ui.viewmodels.AuthViewModel", "import com.example.ui.viewmodels.AuthViewModel\nimport com.example.ui.viewmodels.AuthState")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
