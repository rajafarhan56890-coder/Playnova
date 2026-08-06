package com.example.ui.screens

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.AccountBalanceWallet
import androidx.compose.material.icons.filled.Leaderboard
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.ui.unit.dp
import androidx.compose.material3.Text
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.NavType
import androidx.navigation.navArgument

import androidx.navigation.NavGraph.Companion.findStartDestination

import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.viewmodels.AuthViewModel

@Composable
fun MainDashboardScreen(onLogout: () -> Unit = {}, authViewModel: AuthViewModel = viewModel()) {
    val bottomNavController = rememberNavController()
    val navBackStackEntry by bottomNavController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    Scaffold(
        bottomBar = {
            if (currentRoute != "notifications") {
                NavigationBar(
                    containerColor = androidx.compose.material3.MaterialTheme.colorScheme.surface,
                    tonalElevation = 0.dp,
                    windowInsets = androidx.compose.foundation.layout.WindowInsets(0, 0, 0, 0)
                ) {
                    val navigateTo = { route: String ->
                        if (currentRoute != route) {
                            bottomNavController.navigate(route) {
                                popUpTo(bottomNavController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    }

                    NavigationBarItem(
                        selected = currentRoute == "home",
                        onClick = { navigateTo("home") },
                        icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                        label = { Text("Home") }
                    )
                    NavigationBarItem(
                        selected = currentRoute == "games",
                        onClick = { navigateTo("games") },
                        icon = { Icon(Icons.Default.PlayArrow, contentDescription = "Games") },
                        label = { Text("Games") }
                    )
                    NavigationBarItem(
                        selected = currentRoute == "wallet",
                        onClick = { navigateTo("wallet") },
                        icon = { Icon(Icons.Default.AccountBalanceWallet, contentDescription = "Wallet") },
                        label = { Text("Wallet") }
                    )
                    NavigationBarItem(
                        selected = currentRoute == "leaderboard",
                        onClick = { navigateTo("leaderboard") },
                        icon = { Icon(Icons.Default.Leaderboard, contentDescription = "Leaderboard") },
                        label = { Text("Rank") }
                    )
                    NavigationBarItem(
                        selected = currentRoute == "profile",
                        onClick = { navigateTo("profile") },
                        icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                        label = { Text("Profile") }
                    )
                }
            }
        }
    ) { paddingValues ->
        NavHost(
            navController = bottomNavController,
            startDestination = "home",
            modifier = Modifier.padding(paddingValues),
            enterTransition = { fadeIn(animationSpec = tween(300)) + slideInHorizontally(animationSpec = tween(300)) { 300 } },
            exitTransition = { fadeOut(animationSpec = tween(300)) + slideOutHorizontally(animationSpec = tween(300)) { -300 } },
            popEnterTransition = { fadeIn(animationSpec = tween(300)) + slideInHorizontally(animationSpec = tween(300)) { -300 } },
            popExitTransition = { fadeOut(animationSpec = tween(300)) + slideOutHorizontally(animationSpec = tween(300)) { 300 } }
        ) {
            composable("home") { 
                HomeScreen(onNavigateToNotifications = { bottomNavController.navigate("notifications") }) 
            }
            composable("games") { GamesScreen(onNavigateToGame = { gameId -> bottomNavController.navigate("game_details/$gameId") }) }
                        composable(
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
                route = "play_game/{gameId}",
                arguments = listOf(navArgument("gameId") { type = NavType.StringType })
            ) { backStackEntry ->
                val gameId = backStackEntry.arguments?.getString("gameId") ?: "1"
                MiniGameScreen(
                    gameId = gameId,
                    onBack = { bottomNavController.popBackStack() },
                    onReward = { amount ->
                        authViewModel.addBalance(amount, "Game Reward")
                    }
                )
            }
            composable("wallet") { WalletScreen() }
            composable("leaderboard") { LeaderboardScreen() }
            composable("profile") { ProfileScreen(onLogout = onLogout) }
            composable("notifications") { 
                NotificationsScreen(onBackClick = { bottomNavController.popBackStack() }) 
            }
        }
    }
}
