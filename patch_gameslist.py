with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'r') as f:
    content = f.read()

import re

old_section = re.search(r'@Composable\nfun GamesListSection\(\) \{.*?(?=@Composable\nfun GameCardDetailed)', content, re.DOTALL).group(0)

new_section = """@Composable
fun GamesListSection(onPlayGame: (Game) -> Unit) {
    val categories = listOf("All", "Action", "Puzzle", "Ads", "Strategy", "Arcade")
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
    val filteredGames = mockGames.filter { it.category == currentCategory || currentCategory == "All" }

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
}
"""

content = content.replace(old_section, new_section)

# Also fix the call to GamesListSection in GamesScreen
content = content.replace("        if (selectedTab == 0) {\n            GamesListSection()\n        } else {", "        if (selectedTab == 0) {\n            GamesListSection()\n        } else {")
# Wait, I already replaced that in patch_games.py! Let me check if it's there.
with open('app/src/main/java/com/example/ui/screens/GamesScreen.kt', 'w') as f:
    f.write(content)
