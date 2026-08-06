with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'r') as f:
    content = f.read()

imports_to_add = """
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.viewmodels.AuthViewModel
"""

content = content.replace("import com.example.domain.Game", "import com.example.domain.Game" + imports_to_add)

old_games_screen = """@Composable
fun GamesScreen() {
    var selectedTab by remember { mutableIntStateOf(0) }
    val tabs = listOf("All Games", "Leaderboard")

    Column(
        modifier = Modifier.fillMaxSize()
    ) {
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "Play & Earn",
            style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(horizontal = 16.dp)
        )
        Spacer(modifier = Modifier.height(16.dp))
        
        TabRow(
            selectedTabIndex = selectedTab,
            containerColor = MaterialTheme.colorScheme.background,
            contentColor = MaterialTheme.colorScheme.primary
        ) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedTab == index,
                    onClick = { selectedTab = index },
                    text = { Text(title, fontWeight = FontWeight.Bold) }
                )
            }
        }
        
        if (selectedTab == 0) {
            GamesListSection()
        } else {
            LeaderboardSection()
        }
    }
}"""

new_games_screen = """@Composable
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
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Play & Earn",
                style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.padding(horizontal = 16.dp)
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            TabRow(
                selectedTabIndex = selectedTab,
                containerColor = MaterialTheme.colorScheme.background,
                contentColor = MaterialTheme.colorScheme.primary
            ) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTab == index,
                        onClick = { selectedTab = index },
                        text = { Text(title, fontWeight = FontWeight.Bold) }
                    )
                }
            }
            
            if (selectedTab == 0) {
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

content = content.replace(old_games_screen, new_games_screen)

old_games_list = """@Composable
fun GamesListSection() {
    val categories = listOf("Action", "Puzzle", "Strategy", "Arcade")
    var selectedCategory by remember { mutableIntStateOf(0) }
    
    val mockGames = listOf(
        Game("1", "Galaxy Shooter", "Defend the galaxy from invaders.", "Arcade", 50),
        Game("2", "Block Puzzle", "Clear lines by placing blocks.", "Puzzle", 30),
        Game("3", "Tower Defense", "Build towers to stop enemies.", "Strategy", 100),
        Game("4", "Ninja Dash", "Run and slash your way to victory.", "Action", 75),
        Game("5", "Space Miner", "Mine asteroids for precious gems.", "Arcade", 40)
    )

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(categories.size) { index ->
                    Button(
                        onClick = { selectedCategory = index },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (selectedCategory == index) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            contentColor = if (selectedCategory == index) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                        ),
                        shape = RoundedCornerShape(20.dp)
                    ) {
                        Text(categories[index])
                    }
                }
            }
        }
        
        items(mockGames.size) { index ->
            val game = mockGames[index]
            GameCardDetailed(game)
        }
    }
}"""

new_games_list = """@Composable
fun GamesListSection(onPlayGame: (Game) -> Unit) {
    val categories = listOf("Action", "Puzzle", "Ads", "Strategy", "Arcade")
    var selectedCategory by remember { mutableIntStateOf(0) }
    
    val mockGames = listOf(
        Game("1", "Galaxy Shooter", "Defend the galaxy from invaders.", "Arcade", 50),
        Game("2", "Block Puzzle", "Clear lines by placing blocks.", "Puzzle", 30),
        Game("3", "Tower Defense", "Build towers to stop enemies.", "Strategy", 100),
        Game("4", "Ninja Dash", "Run and slash your way to victory.", "Action", 75),
        Game("5", "Space Miner", "Mine asteroids for precious gems.", "Arcade", 40),
        Game("6", "Watch Video Ad", "Watch a short ad to earn Nova.", "Ads", 25),
        Game("7", "Reward Ad 2", "Bonus reward for watching an ad.", "Ads", 50),
        Game("8", "Offerwall Ad", "Complete simple offers.", "Ads", 150)
    )

    val currentCategory = categories[selectedCategory]
    val filteredGames = mockGames.filter { it.category == currentCategory || currentCategory == "All" } // We don't have "All", just filtering exact match or just show all if we want. Actually let's just filter.

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(categories.size) { index ->
                    Button(
                        onClick = { selectedCategory = index },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (selectedCategory == index) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
                            contentColor = if (selectedCategory == index) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface
                        ),
                        shape = RoundedCornerShape(20.dp)
                    ) {
                        Text(categories[index])
                    }
                }
            }
        }
        
        items(filteredGames.size) { index ->
            val game = filteredGames[index]
            GameCardDetailed(game, onPlayGame)
        }
    }
}"""

content = content.replace(old_games_list, new_games_list)

old_card = """@Composable
fun GameCardDetailed(game: Game) {"""

new_card = """@Composable
fun GameCardDetailed(game: Game, onPlayClick: (Game) -> Unit) {"""
content = content.replace(old_card, new_card)

old_play_click = """Button(
                onClick = { /* Play game */ },
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Play")
            }"""

new_play_click = """Button(
                onClick = { onPlayClick(game) },
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(if (game.category == "Ads") "Watch" else "Play")
            }"""
content = content.replace(old_play_click, new_play_click)

with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'w') as f:
    f.write(content)

