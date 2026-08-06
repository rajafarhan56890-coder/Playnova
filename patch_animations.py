import os

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.animation" not in content:
    imports = """import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
"""
    content = content.replace("import androidx.compose.runtime.Composable", imports + "import androidx.compose.runtime.Composable")

old_navhost = """        NavHost(
            navController = bottomNavController,
            startDestination = "home",
            modifier = Modifier.padding(paddingValues)
        ) {"""

new_navhost = """        NavHost(
            navController = bottomNavController,
            startDestination = "home",
            modifier = Modifier.padding(paddingValues),
            enterTransition = { fadeIn(animationSpec = tween(300)) + slideInHorizontally(animationSpec = tween(300)) { 300 } },
            exitTransition = { fadeOut(animationSpec = tween(300)) + slideOutHorizontally(animationSpec = tween(300)) { -300 } },
            popEnterTransition = { fadeIn(animationSpec = tween(300)) + slideInHorizontally(animationSpec = tween(300)) { -300 } },
            popExitTransition = { fadeOut(animationSpec = tween(300)) + slideOutHorizontally(animationSpec = tween(300)) { 300 } }
        ) {"""

content = content.replace(old_navhost, new_navhost)

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'w') as f:
    f.write(content)
