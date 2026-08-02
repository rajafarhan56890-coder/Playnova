package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.draw.scale
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.viewmodels.AuthState
import com.example.ui.viewmodels.AuthViewModel
import com.example.ui.viewmodels.DailyRewardState
import com.example.ui.viewmodels.DailyRewardViewModel

@Composable
fun HomeScreen(
    onNavigateToNotifications: () -> Unit = {},
    authViewModel: AuthViewModel = viewModel()
) {
    val authState by authViewModel.authState.collectAsState()
    val user = (authState as? AuthState.Success)?.user

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        item {
            Spacer(modifier = Modifier.height(24.dp))
            HeaderSection(user?.username ?: "PlayerOne", onNavigateToNotifications)
        }
        item {
            BalanceCard(user?.balance ?: 0)
        }
        item {
            TrendChartCard(user?.balance ?: 0)
        }
        item {
            DailyRewardCard()
        }
        item {
            Text(
                text = "Featured Quests",
                style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.onBackground
            )
            Spacer(modifier = Modifier.height(12.dp))
            LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                items(3) { index ->
                    QuestCard(title = "Quest ${index + 1}", reward = "${(index + 1) * 100} Nova")
                }
            }
        }
        item {
            Text(
                text = "Recent Games",
                style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.onBackground
            )
            Spacer(modifier = Modifier.height(12.dp))
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                repeat(4) { index ->
                    GameListTile(title = "Galaxy Shooter $index", reward = "+50 Nova")
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

@Composable
fun HeaderSection(username: String, onNavigateToNotifications: () -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                text = "Welcome back,",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f)
            )
            Text(
                text = username,
                style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.onBackground
            )
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = onNavigateToNotifications) {
                Icon(
                    Icons.Default.Notifications,
                    contentDescription = "Notifications",
                    tint = MaterialTheme.colorScheme.onBackground
                )
            }
            Spacer(modifier = Modifier.width(8.dp))
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.primary),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Star, contentDescription = "Avatar", tint = Color.White)
            }
        }
    }
}


@Composable
fun BalanceCard(balance: Long) {
    var previousBalance by remember { mutableStateOf(balance) }
    var scaleMultiplier by remember { mutableStateOf(1f) }

    val scale by animateFloatAsState(
        targetValue = scaleMultiplier,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        )
    )

    LaunchedEffect(balance) {
        if (balance != previousBalance) {
            scaleMultiplier = 1.3f
            kotlinx.coroutines.delay(150)
            scaleMultiplier = 1f
            previousBalance = balance
        }
    }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondary.copy(alpha = 0.1f))
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text(
                text = "Total Balance",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.secondary
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    Icons.Default.Star,
                    contentDescription = "Coin",
                    tint = MaterialTheme.colorScheme.secondary,
                    modifier = Modifier.size(32.dp).scale(scale)
                )
                Spacer(modifier = Modifier.width(8.dp))
                AnimatedContent(
                    targetState = balance,
                    transitionSpec = {
                        if (targetState > initialState) {
                            (slideInVertically { height -> height } + fadeIn()).togetherWith(slideOutVertically { height -> -height } + fadeOut())
                        } else {
                            (slideInVertically { height -> -height } + fadeIn()).togetherWith(slideOutVertically { height -> height } + fadeOut())
                        }.using(SizeTransform(clip = false))
                    },
                    label = "balanceAnimation"
                ) { targetBalance ->
                    Text(
                        text = "$targetBalance",
                        style = MaterialTheme.typography.headlineLarge.copy(fontWeight = FontWeight.Bold),
                        color = MaterialTheme.colorScheme.onBackground
                    )
                }
            }
        }
    }
}

@Composable
fun QuestCard(title: String, reward: String) {
    Card(
        modifier = Modifier.size(160.dp, 120.dp),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(
            modifier = Modifier.padding(16.dp).fillMaxSize(),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurface
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Star, contentDescription = null, tint = MaterialTheme.colorScheme.tertiary, modifier = Modifier.size(16.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(text = reward, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.tertiary)
            }
        }
    }
}

@Composable
fun GameListTile(title: String, reward: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.2f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Star, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurface
            )
        }
        Text(
            text = reward,
            style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Bold),
            color = MaterialTheme.colorScheme.secondary
        )
    }
}

@Composable
fun DailyRewardCard(viewModel: DailyRewardViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.tertiaryContainer)
    ) {
        Row(
            modifier = Modifier.padding(20.dp).fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("Daily Reward", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onTertiaryContainer)
                Spacer(modifier = Modifier.height(4.dp))
                when (uiState) {
                    is DailyRewardState.Loading -> {
                        Text("Loading...", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.7f))
                    }
                    is DailyRewardState.Available -> {
                        Text("Claim +50 Nova!", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.7f))
                    }
                    is DailyRewardState.Claimed -> {
                        val hours = (uiState as DailyRewardState.Claimed).hoursLeft
                        Text("Come back in $hours hours", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onTertiaryContainer.copy(alpha = 0.7f))
                    }
                    is DailyRewardState.Error -> {
                        val msg = (uiState as DailyRewardState.Error).message
                        Text(msg, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
                    }
                }
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
            Button(
                onClick = { viewModel.claimReward() },
                enabled = uiState is DailyRewardState.Available,
                modifier = Modifier.height(40.dp)
            ) {
                if (uiState is DailyRewardState.Loading) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                } else {
                    Text("Claim")
                }
            }
        }
    }
}



@Composable
fun TrendChartCard(currentBalance: Long) {
    val trendData = remember(currentBalance) {
        val data = mutableListOf<Float>()
        var current = currentBalance.toFloat()
        data.add(current)
        for (i in 0..5) {
            current = (current - (10..100).random()).coerceAtLeast(0f)
            data.add(current)
        }
        data.reversed()
    }

    Card(
        modifier = Modifier.fillMaxWidth().height(180.dp),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Text(
                text = "7-Day Trend",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurface
            )
            Spacer(modifier = Modifier.height(16.dp))
            val lineColor = MaterialTheme.colorScheme.secondary
            androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                val max = trendData.maxOrNull() ?: 100f
                val min = trendData.minOrNull() ?: 0f
                val range = (max - min).coerceAtLeast(1f)
                
                val width = size.width
                val height = size.height
                val stepX = width / (trendData.size - 1)
                
                val path = androidx.compose.ui.graphics.Path()
                val fillPath = androidx.compose.ui.graphics.Path()
                
                trendData.forEachIndexed { index, value ->
                    val x = index * stepX
                    val y = height - ((value - min) / range * height)
                    if (index == 0) {
                        path.moveTo(x, y)
                        fillPath.moveTo(x, height)
                        fillPath.lineTo(x, y)
                    } else {
                        path.lineTo(x, y)
                        fillPath.lineTo(x, y)
                    }
                    if (index == trendData.size - 1) {
                        fillPath.lineTo(x, height)
                        fillPath.close()
                    }
                }
                
                drawPath(
                    path = fillPath,
                    brush = androidx.compose.ui.graphics.Brush.verticalGradient(
                        colors = listOf(
                            lineColor.copy(alpha = 0.3f),
                            androidx.compose.ui.graphics.Color.Transparent
                        )
                    )
                )
                
                drawPath(
                    path = path,
                    color = lineColor,
                    style = androidx.compose.ui.graphics.drawscope.Stroke(
                        width = 4.dp.toPx(),
                        cap = androidx.compose.ui.graphics.StrokeCap.Round,
                        join = androidx.compose.ui.graphics.StrokeJoin.Round
                    )
                )
                
                trendData.forEachIndexed { index, value ->
                    val x = index * stepX
                    val y = height - ((value - min) / range * height)
                    drawCircle(
                        color = lineColor,
                        radius = 6.dp.toPx(),
                        center = androidx.compose.ui.geometry.Offset(x, y)
                    )
                    drawCircle(
                        color = androidx.compose.ui.graphics.Color.White,
                        radius = 3.dp.toPx(),
                        center = androidx.compose.ui.geometry.Offset(x, y)
                    )
                }
            }
        }
    }
}
