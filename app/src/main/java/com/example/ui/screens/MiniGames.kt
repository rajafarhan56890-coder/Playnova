package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlin.random.Random

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MiniGameScreen(gameId: String, onBack: () -> Unit, onReward: (Long) -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(getGameName(gameId)) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, "Back")
                    }
                }
            )
        }
    ) { padding ->
        Box(modifier = Modifier.padding(padding).fillMaxSize()) {
            when (gameId) {
                "1" -> TapTapGame(onReward = { onReward(it.toLong()); onBack() })
                "2" -> MemoryGame(onReward = { onReward(it.toLong()); onBack() })
                "3" -> ReactionGame(onReward = { onReward(it.toLong()); onBack() })
                "4" -> ColorMatchGame(onReward = { onReward(it.toLong()); onBack() })
                "5" -> FlappyBirdGame(onReward = { onReward(it.toLong()); onBack() })
                else -> {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("Coming Soon!")
                        Button(onClick = onBack) { Text("Back") }
                    }
                }
            }
        }
    }
}

fun getGameName(id: String): String {
    return when(id) {
        "1" -> "Tap Tap Runner"
        "2" -> "Memory Master"
        "3" -> "Reaction Time"
        "4" -> "Color Match"
        "5" -> "Flappy Nova"
        else -> "Game"
    }
}

@Composable
fun TapTapGame(onReward: (Int) -> Unit) {
    var score by remember { mutableIntStateOf(0) }
    var timeLeft by remember { mutableIntStateOf(10) }
    var isPlaying by remember { mutableStateOf(false) }
    var gameOver by remember { mutableStateOf(false) }

    LaunchedEffect(isPlaying) {
        if (isPlaying) {
            while (timeLeft > 0) {
                delay(1000)
                timeLeft--
            }
            isPlaying = false
            gameOver = true
        }
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        if (!isPlaying && !gameOver) {
            Text("Tap as fast as you can in 10 seconds!", style = MaterialTheme.typography.titleLarge)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = { isPlaying = true; score = 0; timeLeft = 10 }) {
                Text("Start Game")
            }
        } else if (isPlaying) {
            Text("Time: $timeLeft", style = MaterialTheme.typography.headlineMedium)
            Text("Score: $score", style = MaterialTheme.typography.headlineLarge)
            Spacer(modifier = Modifier.height(48.dp))
            Box(
                modifier = Modifier
                    .size(150.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primary)
                    .clickable { score++ },
                contentAlignment = Alignment.Center
            ) {
                Text("TAP!", color = Color.White, style = MaterialTheme.typography.headlineLarge)
            }
        } else if (gameOver) {
            Text("Game Over!", style = MaterialTheme.typography.headlineLarge)
            Text("You tapped $score times.", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = { onReward(score) }) {
                Text("Claim ${score} Nova")
            }
        }
    }
}

@Composable
fun MemoryGame(onReward: (Int) -> Unit) {
    var sequence by remember { mutableStateOf(listOf<Int>()) }
    var playerSequence by remember { mutableStateOf(listOf<Int>()) }
    var isShowingSequence by remember { mutableStateOf(false) }
    var level by remember { mutableIntStateOf(1) }
    var gameOver by remember { mutableStateOf(false) }
    var activeBox by remember { mutableStateOf<Int?>(null) }

    val colors = listOf(Color.Red, Color.Green, Color.Blue, Color.Yellow)

    LaunchedEffect(level, gameOver) {
        if (!gameOver) {
            isShowingSequence = true
            sequence = sequence + Random.nextInt(4)
            playerSequence = emptyList()
            delay(1000)
            for (i in sequence) {
                activeBox = i
                delay(500)
                activeBox = null
                delay(250)
            }
            isShowingSequence = false
        }
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        if (gameOver) {
            Text("Game Over!", style = MaterialTheme.typography.headlineLarge)
            Text("You reached level $level.", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = { onReward(level * 10) }) {
                Text("Claim ${level * 10} Nova")
            }
            return@Column
        }

        Text("Level: $level", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(32.dp))

        Row {
            Box(modifier = Modifier
                .size(100.dp)
                .padding(8.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(if (activeBox == 0) colors[0] else colors[0].copy(alpha = 0.3f))
                .clickable(enabled = !isShowingSequence) {
                    playerSequence = playerSequence + 0
                    if (playerSequence.last() != sequence[playerSequence.size - 1]) gameOver = true
                    else if (playerSequence.size == sequence.size) level++
                })
            Box(modifier = Modifier
                .size(100.dp)
                .padding(8.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(if (activeBox == 1) colors[1] else colors[1].copy(alpha = 0.3f))
                .clickable(enabled = !isShowingSequence) {
                    playerSequence = playerSequence + 1
                    if (playerSequence.last() != sequence[playerSequence.size - 1]) gameOver = true
                    else if (playerSequence.size == sequence.size) level++
                })
        }
        Row {
            Box(modifier = Modifier
                .size(100.dp)
                .padding(8.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(if (activeBox == 2) colors[2] else colors[2].copy(alpha = 0.3f))
                .clickable(enabled = !isShowingSequence) {
                    playerSequence = playerSequence + 2
                    if (playerSequence.last() != sequence[playerSequence.size - 1]) gameOver = true
                    else if (playerSequence.size == sequence.size) level++
                })
            Box(modifier = Modifier
                .size(100.dp)
                .padding(8.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(if (activeBox == 3) colors[3] else colors[3].copy(alpha = 0.3f))
                .clickable(enabled = !isShowingSequence) {
                    playerSequence = playerSequence + 3
                    if (playerSequence.last() != sequence[playerSequence.size - 1]) gameOver = true
                    else if (playerSequence.size == sequence.size) level++
                })
        }
    }
}

@Composable
fun ReactionGame(onReward: (Int) -> Unit) {
    var state by remember { mutableIntStateOf(0) } // 0: Start, 1: Wait, 2: Click, 3: Result
    var startTime by remember { mutableLongStateOf(0L) }
    var reactionTime by remember { mutableLongStateOf(0L) }

    LaunchedEffect(state) {
        if (state == 1) {
            val waitTime = Random.nextLong(2000, 5000)
            delay(waitTime)
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
}

@Composable
fun ColorMatchGame(onReward: (Int) -> Unit) {
    var score by remember { mutableIntStateOf(0) }
    var timeLeft by remember { mutableIntStateOf(30) }
    var isPlaying by remember { mutableStateOf(false) }
    var gameOver by remember { mutableStateOf(false) }
    
    val colorNames = listOf("RED", "GREEN", "BLUE", "YELLOW")
    val colors = listOf(Color.Red, Color.Green, Color.Blue, Color.Yellow)
    
    var wordIndex by remember { mutableIntStateOf(Random.nextInt(4)) }
    var colorIndex by remember { mutableIntStateOf(Random.nextInt(4)) }

    LaunchedEffect(isPlaying) {
        if (isPlaying) {
            while (timeLeft > 0) {
                delay(1000)
                timeLeft--
            }
            isPlaying = false
            gameOver = true
        }
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        if (!isPlaying && !gameOver) {
            Text("Does the word match the color?", style = MaterialTheme.typography.titleLarge)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = { isPlaying = true; score = 0; timeLeft = 30 }) {
                Text("Start Game")
            }
        } else if (isPlaying) {
            Text("Time: $timeLeft", style = MaterialTheme.typography.headlineMedium)
            Text("Score: $score", style = MaterialTheme.typography.headlineLarge)
            Spacer(modifier = Modifier.height(48.dp))
            
            Text(
                text = colorNames[wordIndex],
                color = colors[colorIndex],
                style = MaterialTheme.typography.displayLarge.copy(fontWeight = FontWeight.Bold)
            )
            
            Spacer(modifier = Modifier.height(48.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(onClick = { 
                    if (wordIndex == colorIndex) score += 5 else score -= 5
                    wordIndex = Random.nextInt(4)
                    colorIndex = Random.nextInt(4)
                }) {
                    Text("YES")
                }
                Button(onClick = { 
                    if (wordIndex != colorIndex) score += 5 else score -= 5
                    wordIndex = Random.nextInt(4)
                    colorIndex = Random.nextInt(4)
                }) {
                    Text("NO")
                }
            }
        } else if (gameOver) {
            Text("Game Over!", style = MaterialTheme.typography.headlineLarge)
            Text("Your score: $score", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(24.dp))
            Button(onClick = { onReward(maxOf(0, score)) }) {
                Text("Claim ${maxOf(0, score)} Nova")
            }
        }
    }
}

@Composable
fun FlappyBirdGame(onReward: (Int) -> Unit) {
    var isPlaying by remember { mutableStateOf(false) }
    var gameOver by remember { mutableStateOf(false) }
    var score by remember { mutableIntStateOf(0) }
    
    var birdY by remember { mutableFloatStateOf(0.5f) }
    var birdVelocity by remember { mutableFloatStateOf(0f) }
    var pipeX by remember { mutableFloatStateOf(1f) }
    var pipeGapY by remember { mutableFloatStateOf(0.5f) }
    
    val gravity = 0.005f
    val jumpStrength = -0.05f
    val pipeSpeed = 0.02f
    val pipeWidth = 0.2f
    val pipeGapSize = 0.3f
    
    LaunchedEffect(isPlaying) {
        while (isPlaying) {
            delay(16) // ~60fps
            birdVelocity += gravity
            birdY += birdVelocity
            
            pipeX -= pipeSpeed
            if (pipeX < -pipeWidth) {
                pipeX = 1f
                pipeGapY = Random.nextFloat() * 0.6f + 0.2f
                score++
            }
            
            // Collision detection
            val birdRectTop = birdY - 0.02f
            val birdRectBottom = birdY + 0.02f
            val birdRectLeft = 0.2f - 0.02f
            val birdRectRight = 0.2f + 0.02f
            
            val pipeRectLeft = pipeX
            val pipeRectRight = pipeX + pipeWidth
            
            val hitPipeX = birdRectRight > pipeRectLeft && birdRectLeft < pipeRectRight
            val hitPipeY = birdRectTop < (pipeGapY - pipeGapSize/2) || birdRectBottom > (pipeGapY + pipeGapSize/2)
            
            if ((hitPipeX && hitPipeY) || birdY > 1f || birdY < 0f) {
                isPlaying = false
                gameOver = true
            }
        }
    }
    
    Box(modifier = Modifier
        .fillMaxSize()
        .background(Color.Cyan)
        .clickable {
            if (!isPlaying && !gameOver) {
                isPlaying = true
            } else if (isPlaying) {
                birdVelocity = jumpStrength
            }
        }
    ) {
        if (!isPlaying && !gameOver) {
            Text("Tap to Start & Jump", modifier = Modifier.align(Alignment.Center), style = MaterialTheme.typography.headlineLarge)
        }
        
        // Draw bird
        Box(modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)) {
            androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                val canvasWidth = size.width
                val canvasHeight = size.height
                
                // Draw pipes
                val pipeLeft = pipeX * canvasWidth
                val pipeRight = (pipeX + pipeWidth) * canvasWidth
                val gapCenter = pipeGapY * canvasHeight
                val gapTop = gapCenter - (pipeGapSize/2 * canvasHeight)
                val gapBottom = gapCenter + (pipeGapSize/2 * canvasHeight)
                
                // Top pipe
                drawRect(Color.Green, topLeft = androidx.compose.ui.geometry.Offset(pipeLeft, 0f), size = androidx.compose.ui.geometry.Size(pipeWidth * canvasWidth, gapTop))
                // Bottom pipe
                drawRect(Color.Green, topLeft = androidx.compose.ui.geometry.Offset(pipeLeft, gapBottom), size = androidx.compose.ui.geometry.Size(pipeWidth * canvasWidth, canvasHeight - gapBottom))
                
                // Draw bird
                drawCircle(Color.Yellow, radius = 0.02f * canvasHeight, center = androidx.compose.ui.geometry.Offset(0.2f * canvasWidth, birdY * canvasHeight))
            }
        }
        
        Text("Score: $score", modifier = Modifier.align(Alignment.TopCenter).padding(32.dp), style = MaterialTheme.typography.headlineMedium)
        
        if (gameOver) {
            Column(modifier = Modifier.align(Alignment.Center).background(Color.White.copy(alpha=0.8f)).padding(32.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Game Over!", style = MaterialTheme.typography.headlineLarge)
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { onReward(score * 5) }) {
                    Text("Claim ${score * 5} Nova")
                }
            }
        }
    }
}
