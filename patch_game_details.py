import os
import re

with open('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt', 'r') as f:
    content = f.read()

old_hero = """                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .background(MaterialTheme.colorScheme.primaryContainer),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.PlayArrow,
                        contentDescription = null,
                        modifier = Modifier.size(80.dp),
                        tint = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }"""

new_hero = """                Box(
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
                }"""

content = content.replace(old_hero, new_hero)

with open('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt', 'w') as f:
    f.write(content)

