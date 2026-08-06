with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'r') as f:
    content = f.read()

import re

old_sig = "fun MainDashboardScreen(onLogout: () -> Unit = {}) {"
new_sig = """import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.viewmodels.AuthViewModel

@Composable
fun MainDashboardScreen(onLogout: () -> Unit = {}, authViewModel: AuthViewModel = viewModel()) {"""

content = content.replace("@Composable\nfun MainDashboardScreen(onLogout: () -> Unit = {}) {", new_sig)

old_reward = """                    onReward = { amount ->
                        // Reward is handled inside the game by passing to ViewModel?
                        // Wait, we can pass AuthViewModel to MiniGameScreen, or handle it here
                        // Let's pass the viewmodel
                    }"""

new_reward = """                    onReward = { amount ->
                        authViewModel.addBalance(amount, "Game Reward")
                    }"""

content = content.replace(old_reward, new_reward)

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'w') as f:
    f.write(content)
