import os

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'r') as f:
    content = f.read()

import re

old_nav = """                NavigationBar(
                    containerColor = androidx.compose.material3.MaterialTheme.colorScheme.surface,
                    tonalElevation = 8.dp,
                    windowInsets = androidx.compose.foundation.layout.WindowInsets(0, 0, 0, 0)
                ) {"""

new_nav = """                NavigationBar(
                    containerColor = androidx.compose.material3.MaterialTheme.colorScheme.surface,
                    tonalElevation = 0.dp,
                    windowInsets = androidx.compose.foundation.layout.WindowInsets(0, 0, 0, 0)
                ) {"""

content = content.replace(old_nav, new_nav)

with open('app/src/main/java/com/example/ui/screens/MainDashboardScreen.kt', 'w') as f:
    f.write(content)

