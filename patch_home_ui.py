import os

home_screen = """package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.viewmodels.AuthViewModel
import com.example.ui.viewmodels.AuthState
import com.example.ui.viewmodels.DailyRewardState
import com.example.ui.viewmodels.DailyRewardViewModel
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    authViewModel: AuthViewModel = viewModel(),
    onNavigateToNotifications: () -> Unit = {}
) {
    val authState by authViewModel.authState.collectAsState()
    val user = (authState as? AuthState.Success)?.user

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(32.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(MaterialTheme.colorScheme.primary),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color.White, modifier = Modifier.size(20.dp))
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(text = "Pinjoy", style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold))
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
                actions = {
                    IconButton(onClick = onNavigateToNotifications) {
                        Icon(Icons.Default.Notifications, contentDescription = "Notifications", tint = MaterialTheme.colorScheme.onBackground)
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(padding),
            contentPadding = PaddingValues(bottom = 100.dp)
        ) {
            item {
                Spacer(modifier = Modifier.height(8.dp))
                BalanceHeroCard(user?.balance ?: 0)
            }
            item {
                Spacer(modifier = Modifier.height(32.dp))
                SectionTitle("Daily Rewards")
                DailyRewardCard()
            }
            item {
                Spacer(modifier = Modifier.height(32.dp))
                SectionTitle("Hot Games")
                FeaturedGamesRow()
            }
            item {
                Spacer(modifier = Modifier.height(32.dp))
                SectionTitle("Recent Earnings")
                RecentActivityList()
            }
        }
    }
}

@Composable
fun BalanceHeroCard(balance: Long) {
    val formattedBalance = NumberFormat.getNumberInstance(Locale.US).format(balance)
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
            .clip(RoundedCornerShape(28.dp))
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.primary,
                        Color(0xFF818CF8) // Lighter indigo
                    )
                )
            )
            .padding(24.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                "Total Earnings",
                style = MaterialTheme.typography.titleMedium,
                color = Color.White.copy(alpha = 0.8f)
            )
            Spacer(modifier = Modifier.height(12.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    Icons.Default.Star,
                    contentDescription = null,
                    tint = Color(0xFFFBBF24), // Gold/Amber
                    modifier = Modifier.size(40.dp)
                )
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = formattedBalance,
                    style = MaterialTheme.typography.displayMedium.copy(fontWeight = FontWeight.Black),
                    color = Color.White
                )
            }
            Spacer(modifier = Modifier.height(24.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = { /* TODO withdraw */ },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.White, contentColor = MaterialTheme.colorScheme.primary),
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.weight(1f).height(54.dp)
                ) {
                    Text("Withdraw", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold))
                }
                Button(
                    onClick = { /* TODO earn */ },
                    colors = ButtonDefaults.buttonColors(containerColor = Color.White.copy(alpha = 0.2f), contentColor = Color.White),
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.weight(1f).height(54.dp),
                    elevation = null
                ) {
                    Text("Earn More", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold))
                }
            }
        }
    }
}

@Composable
fun SectionTitle(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
        modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp),
        color = MaterialTheme.colorScheme.onBackground
    )
}

@Composable
fun FeaturedGamesRow() {
    LazyRow(
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(3) { index ->
            FeaturedGameCard(index)
        }
    }
}

@Composable
fun FeaturedGameCard(index: Int) {
    val titles = listOf("Coin Dash", "Memory Match", "Speed Tap")
    val colors = listOf(
        MaterialTheme.colorScheme.primary,
        MaterialTheme.colorScheme.tertiary,
        MaterialTheme.colorScheme.secondary
    )
    
    Card(
        modifier = Modifier
            .width(170.dp)
            .clickable { },
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(130.dp)
                    .background(colors[index].copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Box(
                    modifier = Modifier
                        .size(64.dp)
                        .clip(CircleShape)
                        .background(colors[index]),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        Icons.Default.PlayArrow,
                        contentDescription = null,
                        modifier = Modifier.size(32.dp),
                        tint = Color.White
                    )
                }
            }
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = titles[index],
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onBackground,
                    maxLines = 1
                )
                Spacer(modifier = Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Star, contentDescription = null, tint = Color(0xFFFBBF24), modifier = Modifier.size(16.dp))
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("Up to 1,000", style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Medium), color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

@Composable
fun DailyRewardCard(viewModel: DailyRewardViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Row(
            modifier = Modifier.padding(20.dp).fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .clip(RoundedCornerShape(16.dp))
                        .background(MaterialTheme.colorScheme.tertiaryContainer),
                    contentAlignment = Alignment.Center
                ) {
                    Text("🎁", style = MaterialTheme.typography.headlineMedium)
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column {
                    Text("Daily Gift", style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold), color = MaterialTheme.colorScheme.onBackground)
                    Spacer(modifier = Modifier.height(4.dp))
                    when (uiState) {
                        is DailyRewardState.Loading -> Text("Loading...", style = MaterialTheme.typography.bodyMedium)
                        is DailyRewardState.Available -> Text("Claim your +50 Coins!", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        is DailyRewardState.Claimed -> {
                            val hours = (uiState as DailyRewardState.Claimed).hoursLeft
                            Text("Ready in $hours hours", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        is DailyRewardState.Error -> Text("Error", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                    }
                }
            }
            Spacer(modifier = Modifier.width(12.dp))
            Button(
                onClick = { viewModel.claimReward() },
                enabled = uiState is DailyRewardState.Available,
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Claim", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun RecentActivityList() {
    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
        repeat(3) {
            ActivityTile("Played Tap Tap Runner", "+100")
            Spacer(modifier = Modifier.height(12.dp))
        }
    }
}

@Composable
fun ActivityTile(title: String, amount: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(20.dp))
            .background(MaterialTheme.colorScheme.surface)
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.PlayArrow, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(title, style = MaterialTheme.typography.bodyLarge.copy(fontWeight = FontWeight.Bold), color = MaterialTheme.colorScheme.onBackground)
                Text("Just now", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        Text(amount, style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold), color = MaterialTheme.colorScheme.secondary)
    }
}
"""

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(home_screen)

