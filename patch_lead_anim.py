import os

with open('app/src/main/java/com/example/ui/screens/LeaderboardScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.animation.animateContentSize" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.animation.animateContentSize")

old_lazy = """                    LazyColumn(
                        contentPadding = PaddingValues(bottom = 100.dp)
                    ) {"""

new_lazy = """                    LazyColumn(
                        contentPadding = PaddingValues(bottom = 100.dp),
                        modifier = Modifier.animateContentSize()
                    ) {"""

content = content.replace(old_lazy, new_lazy)

with open('app/src/main/java/com/example/ui/screens/LeaderboardScreen.kt', 'w') as f:
    f.write(content)
