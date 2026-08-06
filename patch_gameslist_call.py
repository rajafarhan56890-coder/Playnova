with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'r') as f:
    content = f.read()

old_call = """        if (selectedTab == 0) {
            GamesListSection()
        } else {"""

new_call = """        if (selectedTab == 0) {
            GamesListSection(onPlayGame = { game -> 
                authViewModel.addBalance(game.rewardPoints.toLong(), "Reward: ${game.title}")
                coroutineScope.launch {
                    snackbarHostState.showSnackbar("You played ${game.title} and earned ${game.rewardPoints} Nova!")
                }
            })
        } else {"""

content = content.replace(old_call, new_call)

with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'w') as f:
    f.write(content)
