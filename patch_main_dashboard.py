with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'r') as f:
    content = f.read()

imports = """
import androidx.navigation.NavType
import androidx.navigation.navArgument
"""

content = content.replace("import androidx.navigation.compose.rememberNavController", "import androidx.navigation.compose.rememberNavController" + imports)

old_nav = """            composable("games") { GamesScreen() }"""
new_nav = """            composable("games") { GamesScreen(onNavigateToGame = { gameId -> bottomNavController.navigate("play_game/$gameId") }) }
            composable(
                route = "play_game/{gameId}",
                arguments = listOf(navArgument("gameId") { type = NavType.StringType })
            ) { backStackEntry ->
                val gameId = backStackEntry.arguments?.getString("gameId") ?: "1"
                MiniGameScreen(
                    gameId = gameId,
                    onBack = { bottomNavController.popBackStack() },
                    onReward = { amount ->
                        // Reward is handled inside the game by passing to ViewModel?
                        // Wait, we can pass AuthViewModel to MiniGameScreen, or handle it here
                        // Let's pass the viewmodel
                    }
                )
            }"""

content = content.replace(old_nav, new_nav)

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'w') as f:
    f.write(content)
