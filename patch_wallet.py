import os
import re

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    content = f.read()

old_card = """    Card(
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                Icons.Default.AccountBalanceWallet,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.size(48.dp).scale(scale)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
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
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
                Text(
                    text = " Nova",
                    style = MaterialTheme.typography.headlineLarge.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "≈ $usdValue USD / $pkrValue PKR",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.8f)
            )
            Spacer(modifier = Modifier.height(24.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = onWithdrawClick,
                    modifier = Modifier.weight(1f).height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary, contentColor = MaterialTheme.colorScheme.onSecondary)
                ) {
                    Text("Withdraw")
                }
                Button(
                    onClick = { /* Handle Redeem items */ },
                    modifier = Modifier.weight(1f).height(50.dp)
                ) {
                    Text("Redeem")
                }
            }
        }
    }"""

new_card = """    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(32.dp))
            .background(
                androidx.compose.ui.graphics.Brush.linearGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.primary,
                        MaterialTheme.colorScheme.secondary
                    )
                )
            )
            .padding(24.dp)
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.fillMaxWidth()
        ) {
            Icon(
                Icons.Default.AccountBalanceWallet,
                contentDescription = null,
                tint = androidx.compose.ui.graphics.Color.White.copy(alpha = 0.8f),
                modifier = Modifier.size(48.dp).scale(scale)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
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
                        color = androidx.compose.ui.graphics.Color.White
                    )
                }
                Text(
                    text = " Nova",
                    style = MaterialTheme.typography.headlineLarge.copy(fontWeight = FontWeight.Bold),
                    color = androidx.compose.ui.graphics.Color.White
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "≈ $usdValue USD / $pkrValue PKR",
                style = MaterialTheme.typography.titleMedium,
                color = androidx.compose.ui.graphics.Color.White.copy(alpha = 0.8f)
            )
            Spacer(modifier = Modifier.height(24.dp))
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = onWithdrawClick,
                    modifier = Modifier.weight(1f).height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = androidx.compose.ui.graphics.Color.White, contentColor = MaterialTheme.colorScheme.primary)
                ) {
                    Text("Withdraw", fontWeight = FontWeight.Bold)
                }
                Button(
                    onClick = { /* Handle Redeem items */ },
                    modifier = Modifier.weight(1f).height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = androidx.compose.ui.graphics.Color.White.copy(alpha = 0.2f), contentColor = androidx.compose.ui.graphics.Color.White)
                ) {
                    Text("Redeem", fontWeight = FontWeight.Bold)
                }
            }
        }
    }"""

content = content.replace(old_card, new_card)

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(content)
