import os

def fix_arrowback(filepath):
    with open(filepath, 'r') as f:
        c = f.read()
    c = c.replace("androidx.compose.material.icons.automirrored.filled.ArrowBack", "Icons.AutoMirrored.Filled.ArrowBack")
    with open(filepath, 'w') as f:
        f.write(c)

fix_arrowback('app/src/main/java/com/example/ui/screens/MiniGames.kt')
fix_arrowback('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt')
