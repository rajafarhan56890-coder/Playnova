with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'r') as f:
    content = f.read()

import re

# We need to change the signature of GamesScreen to take onNavigateToGame: (String) -> Unit
content = re.sub(r'fun GamesScreen\(authViewModel: AuthViewModel = viewModel\(\)\) \{',
                 'fun GamesScreen(authViewModel: AuthViewModel = viewModel(), onNavigateToGame: (String) -> Unit = {}) {',
                 content)

# We need to change GamesListSection call in GamesScreen
old_call = """        if (selectedTab == 0) {
            GamesListSection(onPlayGame = { game -> 
                authViewModel.addBalance(game.rewardPoints.toLong(), "Reward: ${game.title}")
                coroutineScope.launch {
                    snackbarHostState.showSnackbar("You played ${game.title} and earned ${game.rewardPoints} Nova!")
                }
            })
        }"""
new_call = """        if (selectedTab == 0) {
            GamesListSection(onPlayGame = { game -> 
                if (game.id in listOf("1", "2", "3", "4", "5")) {
                    onNavigateToGame(game.id)
                } else {
                    authViewModel.addBalance(game.rewardPoints.toLong(), "Reward: ${game.title}")
                    coroutineScope.launch {
                        snackbarHostState.showSnackbar("You played ${game.title} and earned ${game.rewardPoints} Nova!")
                    }
                }
            })
        }"""
content = content.replace(old_call, new_call)

# We need to change the mockGames list in GamesListSection
old_mockGames = """    val mockGames = listOf(
        Game("1", "Galaxy Shooter", "Defend the galaxy from invaders.", "Arcade", 50),
        Game("2", "Block Puzzle", "Clear lines by placing blocks.", "Puzzle", 30),
        Game("3", "Tower Defense", "Build towers to stop enemies.", "Strategy", 100),
        Game("4", "Ninja Dash", "Run and slash your way to victory.", "Action", 75),
        Game("5", "Space Miner", "Mine asteroids for precious gems.", "Arcade", 40),
        Game("6", "Watch Video Ad", "Watch a short ad to earn Nova.", "Ads", 25),
        Game("7", "Reward Ad 2", "Bonus reward for watching an ad.", "Ads", 50),
        Game("8", "Offerwall Ad", "Complete simple offers.", "Ads", 150)
    )"""

new_mockGames = """    val mockGames = listOf(
        Game("1", "Tap Tap Runner", "Tap as fast as you can in 10 seconds!", "Action", 0),
        Game("2", "Memory Master", "Memorize the sequence of colors.", "Puzzle", 0),
        Game("3", "Reaction Time", "Test your reaction time.", "Action", 0),
        Game("4", "Color Match", "Does the color match the word?", "Puzzle", 0),
        Game("5", "Flappy Nova", "Fly through the pipes!", "Arcade", 0),
        Game("6", "Watch Video Ad", "Watch a short ad to earn Nova.", "Ads", 25),
        Game("7", "Offerwall", "Complete simple offers.", "Ads", 150)
    )"""

content = content.replace(old_mockGames, new_mockGames)

with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'w') as f:
    f.write(content)
