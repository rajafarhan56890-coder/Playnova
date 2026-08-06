package com.example.ui.screens

import androidx.compose.foundation.background
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountBalanceWallet
import androidx.compose.material.icons.filled.ArrowDownward
import androidx.compose.material.icons.filled.ArrowUpward
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.draw.scale
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.domain.Transaction
import com.example.ui.viewmodels.AdminConfig
import com.example.ui.viewmodels.WalletState
import com.example.ui.viewmodels.WalletViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun WalletScreen(walletViewModel: WalletViewModel = viewModel()) {
    val walletState by walletViewModel.walletState.collectAsState()
    val withdrawMessage by walletViewModel.withdrawState.collectAsState()
    var showWithdrawDialog by remember { mutableStateOf(false) }
    var showMessageDialog by remember { mutableStateOf(false) }
    var messageDialogText by remember { mutableStateOf("") }

    LaunchedEffect(withdrawMessage) {
        if (withdrawMessage != null) {
            messageDialogText = withdrawMessage!!
            showMessageDialog = true
            showWithdrawDialog = false
            walletViewModel.clearWithdrawState()
        }
    }

    if (showMessageDialog) {
        AlertDialog(
            onDismissRequest = { showMessageDialog = false },
            title = { Text("Notice") },
            text = { Text(messageDialogText) },
            confirmButton = {
                TextButton(onClick = { showMessageDialog = false }) {
                    Text("OK")
                }
            }
        )
    }

    if (showWithdrawDialog) {
        WithdrawDialog(
            onDismiss = { showWithdrawDialog = false },
            onSubmit = { amount, method, details ->
                walletViewModel.requestWithdrawal(amount, method, details)
            }
        )
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp)
    ) {
        item {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Wallet",
                style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            when (val state = walletState) {
                is WalletState.Loading -> {
                    Box(modifier = Modifier.fillMaxWidth().height(300.dp), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                is WalletState.Error -> {
                    Text("Error: ${state.message}", color = MaterialTheme.colorScheme.error)
                }
                is WalletState.Success -> {
                    WalletBalanceCard(state.balance, state.config) {
                        showWithdrawDialog = true
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    Text(
                        text = "Recent Transactions",
                        style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold),
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }

        if (walletState is WalletState.Success) {
            val transactions = (walletState as WalletState.Success).transactions
            if (transactions.isEmpty()) {
                item {
                    Text(
                        "No transactions yet.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                    )
                }
            } else {
                items(transactions.size) { index ->
                    val transaction = transactions[index]
                    TransactionItemDetailed(
                        title = transaction.title,
                        amount = if (transaction.isPositive) "+${transaction.amount}" else "-${transaction.amount}",
                        isPositive = transaction.isPositive,
                        date = transaction.timestamp,
                        status = transaction.status
                    )
                }
            }
        }
    }
}

@Composable
fun WalletBalanceCard(balance: Long, config: AdminConfig, onWithdrawClick: () -> Unit) {
    val usdValue = String.format(Locale.US, "%.2f", balance * config.conversionRateUSD)
    val pkrValue = String.format(Locale.US, "%.2f", balance * config.conversionRatePKR)

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

    Box(
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
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WithdrawDialog(onDismiss: () -> Unit, onSubmit: (Long, String, String) -> Unit) {
    var amountStr by remember { mutableStateOf("") }
    var accountDetails by remember { mutableStateOf("") }
    var expanded by remember { mutableStateOf(false) }
    var selectedMethod by remember { mutableStateOf("EasyPaisa") }
    val methods = listOf("EasyPaisa", "JazzCash")

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Request Withdrawal") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                OutlinedTextField(
                    value = amountStr,
                    onValueChange = { amountStr = it },
                    label = { Text("Amount (Nova)") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )

                ExposedDropdownMenuBox(
                    expanded = expanded,
                    onExpandedChange = { expanded = it },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    OutlinedTextField(
                        value = selectedMethod,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Payment Method") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                        colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors(),
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable)
                    )
                    ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false }
                    ) {
                        methods.forEach { method ->
                            DropdownMenuItem(
                                text = { Text(method) },
                                onClick = {
                                    selectedMethod = method
                                    expanded = false
                                }
                            )
                        }
                    }
                }

                OutlinedTextField(
                    value = accountDetails,
                    onValueChange = { accountDetails = it },
                    label = { Text("Account Number / Details") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(onClick = {
                val amount = amountStr.toLongOrNull() ?: 0L
                onSubmit(amount, selectedMethod, accountDetails)
            }) {
                Text("Submit")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun TransactionItemDetailed(title: String, amount: String, isPositive: Boolean, date: Date, status: String) {
    val formatter = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
            .clip(RoundedCornerShape(20.dp))
            .background(MaterialTheme.colorScheme.surface)
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(
                        if (isPositive) MaterialTheme.colorScheme.secondary.copy(alpha = 0.15f)
                        else MaterialTheme.colorScheme.error.copy(alpha = 0.15f)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (isPositive) Icons.Default.ArrowDownward else Icons.Default.ArrowUpward,
                    contentDescription = null,
                    tint = if (isPositive) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.error
                )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onBackground
                )
                Text(
                    text = "${formatter.format(date)} • ${status.replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() }}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        Text(
            text = amount,
            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Black),
            color = if (isPositive) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.error
        )
    }
}

