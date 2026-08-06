import os

game_details_code = """package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GameDetailsScreen(gameId: String, onBack: () -> Unit, onPlay: () -> Unit) {
    val gameName = getGameName(gameId)
    val gameDesc = getGameDesc(gameId)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(gameName) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            Box(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                Button(
                    onClick = onPlay,
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Text("Play Game", style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = null,
                        modifier = Modifier.size(80.dp),
                        tint = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
            
            item {
                Text(
                    text = gameName,
                    style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onBackground
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = gameDesc,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f)
                )
            }

            item {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Tasks & Rewards",
                    style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.primary
                )
            }

            item { TaskCard("Reach Level/Score 10", "100 Nova") }
            item { TaskCard("Reach Level/Score 20", "200 Nova") }
            item { TaskCard("Reach Level/Score 50", "500 Nova") }
            item { TaskCard("Reach Level/Score 100", "1000 Nova") }
            
            item { Spacer(modifier = Modifier.height(80.dp)) }
        }
    }
}

@Composable
fun TaskCard(title: String, reward: String) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(16.dp).fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurface
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Star, contentDescription = null, tint = MaterialTheme.colorScheme.tertiary, modifier = Modifier.size(20.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(
                    text = reward,
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.tertiary
                )
            }
        }
    }
}

fun getGameDesc(id: String): String {
    return when(id) {
        "1" -> "Tap as fast as you can in 10 seconds! Reach higher scores to unlock massive rewards."
        "2" -> "Test your memory! Memorize the sequence of colors and repeat it. Higher levels give more coins."
        "3" -> "How fast is your reaction? Test your reflexes. Quick consecutive reactions equal big rewards."
        "4" -> "Does the color match the word? Keep your brain sharp and score high for the ultimate prize."
        "5" -> "Fly through the obstacles without hitting them! Pass more pipes for bigger rewards."
        else -> "Play this amazing game and earn Nova!"
    }
}
"""

with open('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt', 'w') as f:
    f.write(game_details_code)

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'r') as f:
    dashboard_content = f.read()

dashboard_content = dashboard_content.replace(
    'composable("games") { GamesScreen(onNavigateToGame = { gameId -> bottomNavController.navigate("play_game/$gameId") }) }',
    'composable("games") { GamesScreen(onNavigateToGame = { gameId -> bottomNavController.navigate("game_details/$gameId") }) }'
)

new_route = """            composable(
                route = "game_details/{gameId}",
                arguments = listOf(navArgument("gameId") { type = NavType.StringType })
            ) { backStackEntry ->
                val gameId = backStackEntry.arguments?.getString("gameId") ?: "1"
                GameDetailsScreen(
                    gameId = gameId,
                    onBack = { bottomNavController.popBackStack() },
                    onPlay = { bottomNavController.navigate("play_game/$gameId") }
                )
            }
            composable(
                route = "play_game/{gameId}"""

dashboard_content = dashboard_content.replace('composable(\n                route = "play_game/{gameId}', new_route)

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'w') as f:
    f.write(dashboard_content)

with open('app/src/main/java/com/example/ui/screens/MiniGames.kt', 'r') as f:
    minigames_content = f.read()

minigames_content = minigames_content.replace('onReward(score)', 'onReward(score * 10)')
minigames_content = minigames_content.replace('onReward(maxOf(0, score))', 'onReward(maxOf(0, score * 10))')
minigames_content = minigames_content.replace('Claim ${maxOf(0, score)} Nova', 'Claim ${maxOf(0, score * 10)} Nova')
minigames_content = minigames_content.replace('onReward(score * 5)', 'onReward(score * 10)')
minigames_content = minigames_content.replace('Claim ${score * 5} Nova', 'Claim ${score * 10} Nova')

old_reaction = """@Composable
fun ReactionGame(onReward: (Int) -> Unit) {
    var state by remember { mutableIntStateOf(0) } // 0: Start, 1: Wait, 2: Click, 3: Result
    var startTime by remember { mutableLongStateOf(0L) }
    var reactionTime by remember { mutableLongStateOf(0L) }

    LaunchedEffect(state) {
        if (state == 1) {
            val waitTime = kotlin.random.Random.nextLong(2000, 5000)
            kotlinx.coroutines.delay(waitTime)
            state = 2
            startTime = System.currentTimeMillis()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                when (state) {
                    1 -> Color.Red
                    2 -> Color.Green
                    else -> MaterialTheme.colorScheme.background
                }
            )
            .clickable {
                if (state == 0) state = 1
                else if (state == 1) {
                    // clicked too early
                    state = 3
                    reactionTime = -1
                } else if (state == 2) {
                    reactionTime = System.currentTimeMillis() - startTime
                    state = 3
                } else if (state == 3) {
                    state = 0
                }
            },
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = when (state) {
                    0 -> "Tap anywhere to start"
                    1 -> "Wait for green..."
                    2 -> "TAP NOW!"
                    3 -> if (reactionTime == -1L) "Too early!" else "${reactionTime}ms"
                    else -> ""
                },
                style = MaterialTheme.typography.headlineLarge,
                color = if (state == 1 || state == 2) Color.White else MaterialTheme.colorScheme.onBackground
            )
            if (state == 3 && reactionTime > 0) {
                Spacer(modifier = Modifier.height(24.dp))
                val reward = maxOf(0, 50 - (reactionTime / 10).toInt())
                Button(onClick = { onReward(reward) }) {
                    Text("Claim $reward Nova")
                }
            }
        }
    }
}"""

# Since Random was imported as kotlin.random.Random or just Random, let's use a safer regex or just write it fresh since the old block might have slight variations (like delay vs kotlinx.coroutines.delay)

import re

new_reaction = """@Composable
fun ReactionGame(onReward: (Int) -> Unit) {
    var state by remember { mutableIntStateOf(0) } // 0: Start, 1: Wait, 2: Click, 3: Result
    var score by remember { mutableIntStateOf(0) }
    var startTime by remember { mutableLongStateOf(0L) }
    var gameOver by remember { mutableStateOf(false) }

    LaunchedEffect(state) {
        if (state == 1) {
            val waitTime = kotlin.random.Random.nextLong(1000, 3000)
            kotlinx.coroutines.delay(waitTime)
            state = 2
            startTime = System.currentTimeMillis()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                when (state) {
                    1 -> Color.Red
                    2 -> Color.Green
                    else -> MaterialTheme.colorScheme.background
                }
            )
            .clickable {
                if (gameOver) return@clickable
                if (state == 0 || state == 3) {
                    state = 1
                }
                else if (state == 1) {
                    gameOver = true
                } else if (state == 2) {
                    val reactionTime = System.currentTimeMillis() - startTime
                    if (reactionTime < 500) {
                        score++
                        state = 3
                    } else {
                        gameOver = true
                    }
                }
            },
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            if (gameOver) {
                Text("Game Over!", style = MaterialTheme.typography.headlineLarge)
                Text("Score: $score", style = MaterialTheme.typography.headlineMedium)
                Spacer(modifier = Modifier.height(24.dp))
                Button(onClick = { onReward(score * 10) }) {
                    Text("Claim ${score * 10} Nova")
                }
            } else {
                Text(
                    text = when (state) {
                        0 -> "Tap to start"
                        1 -> "Wait for green..."
                        2 -> "TAP NOW!"
                        3 -> "Good! Tap to continue"
                        else -> ""
                    },
                    style = MaterialTheme.typography.headlineLarge,
                    color = if (state == 1 || state == 2) Color.White else MaterialTheme.colorScheme.onBackground
                )
                Spacer(modifier = Modifier.height(16.dp))
                Text("Score: $score", style = MaterialTheme.typography.titleLarge, color = if (state == 1 || state == 2) Color.White else MaterialTheme.colorScheme.onBackground)
            }
        }
    }
}"""

# Using regex to replace ReactionGame completely
minigames_content = re.sub(r'@Composable\nfun ReactionGame\(.*?\n}\n(?=@Composable|\Z)', new_reaction + '\n', minigames_content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/MiniGames.kt', 'w') as f:
    f.write(minigames_content)

