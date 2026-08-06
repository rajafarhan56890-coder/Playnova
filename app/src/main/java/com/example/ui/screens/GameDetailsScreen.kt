package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
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
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
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
                        .height(240.dp)
                        .clip(RoundedCornerShape(32.dp))
                        .background(
                            androidx.compose.ui.graphics.Brush.linearGradient(
                                colors = listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.secondary)
                            )
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = null,
                        modifier = Modifier.size(100.dp),
                        tint = androidx.compose.ui.graphics.Color.White
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

            item { TaskCard("Reach Level/Score 10", "100 Nova", 1f) }
            item { TaskCard("Reach Level/Score 20", "200 Nova", 0.6f) }
            item { TaskCard("Reach Level/Score 50", "500 Nova", 0.1f) }
            item { TaskCard("Reach Level/Score 100", "1000 Nova", 0f) }
            
            item { Spacer(modifier = Modifier.height(80.dp)) }
        }
    }
}

@Composable
fun TaskCard(title: String, reward: String, progress: Float = 0f) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
            Row(
                modifier = Modifier.fillMaxWidth(),
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
            Spacer(modifier = Modifier.height(12.dp))
            LinearProgressIndicator(
                progress = { progress },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(RoundedCornerShape(4.dp)),
                color = MaterialTheme.colorScheme.primary,
                trackColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "${(progress * 100).toInt()}% completed",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
            )
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
