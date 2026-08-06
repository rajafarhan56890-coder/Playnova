package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

data class Game(val id: String, val title: String, val description: String, val imageColors: List<Color>)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GamesScreen(onNavigateToGame: (String) -> Unit) {
    val primaryColor = MaterialTheme.colorScheme.primary
    val secondaryColor = MaterialTheme.colorScheme.secondary
    val tertiaryColor = MaterialTheme.colorScheme.tertiary
    
    val games = listOf(
        Game("1", "Tap Tap Runner", "Fast paced action", listOf(primaryColor, secondaryColor)),
        Game("2", "Memory Master", "Train your brain", listOf(tertiaryColor, primaryColor)),
        Game("3", "Reaction Time", "Quick reflexes", listOf(secondaryColor, tertiaryColor)),
        Game("4", "Color Match", "Focus & Match", listOf(Color(0xFF00CEC9), Color(0xFF6C5CE7))),
        Game("5", "Flappy Coin", "Avoid pipes", listOf(Color(0xFFFFC312), Color(0xFFFD79A8)))
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Arcade", style = MaterialTheme.typography.titleLarge) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                contentPadding = PaddingValues(16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(games) { game ->
                    GameGridCard(game = game, onClick = { onNavigateToGame(game.id) })
                }
            }
        }
    }
}

@Composable
fun GameGridCard(game: Game, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(0.85f)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .background(Brush.verticalGradient(colors = game.imageColors)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.PlayArrow,
                    contentDescription = null,
                    modifier = Modifier.size(48.dp),
                    tint = Color.White
                )
            }
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(12.dp)
            ) {
                Text(
                    text = game.title,
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Star,
                        contentDescription = null,
                        tint = Color(0xFFFFC312),
                        modifier = Modifier.size(14.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "Play to earn",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                    )
                }
            }
        }
    }
}
