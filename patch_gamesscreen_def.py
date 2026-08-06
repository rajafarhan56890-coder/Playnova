import re
with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'r') as f:
    content = f.read()

old_fun = r"""@Composable
fun GamesScreen\(\) \{
    var selectedTab by remember \{ mutableIntStateOf\(0\) \}
    val tabs = listOf\("All Games", "Leaderboard"\)

    Column\(
        modifier = Modifier.fillMaxSize\(\)
    \) \{"""

new_fun = """@Composable
fun GamesScreen(authViewModel: AuthViewModel = viewModel()) {
    var selectedTab by remember { mutableIntStateOf(0) }
    val tabs = listOf("All Games", "Leaderboard")
    val snackbarHostState = remember { SnackbarHostState() }
    val coroutineScope = rememberCoroutineScope()

    Scaffold(
        snackbarHost = { SnackbarHost(hostState = snackbarHostState) },
        containerColor = androidx.compose.ui.graphics.Color.Transparent
    ) { padding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(padding)
        ) {"""

content = re.sub(old_fun, new_fun, content)

# And close the Scaffold block
old_close = """        if (selectedTab == 0) {
            GamesListSection(onPlayGame = { game -> 
                authViewModel.addBalance(game.rewardPoints.toLong(), "Reward: ${game.title}")
                coroutineScope.launch {
                    snackbarHostState.showSnackbar("You played ${game.title} and earned ${game.rewardPoints} Nova!")
                }
            })
        } else {
            LeaderboardSection()
        }
    }
}"""

new_close = """        if (selectedTab == 0) {
            GamesListSection(onPlayGame = { game -> 
                authViewModel.addBalance(game.rewardPoints.toLong(), "Reward: ${game.title}")
                coroutineScope.launch {
                    snackbarHostState.showSnackbar("You played ${game.title} and earned ${game.rewardPoints} Nova!")
                }
            })
        } else {
            LeaderboardSection()
        }
    }
    }
}"""
content = content.replace(old_close, new_close)

with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'w') as f:
    f.write(content)

