import os

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.foundation.shape.CircleShape" not in content:
    content = content.replace("import androidx.compose.foundation.shape.RoundedCornerShape", "import androidx.compose.foundation.shape.RoundedCornerShape\nimport androidx.compose.foundation.shape.CircleShape")

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(content)

def fix_arrowback(filepath):
    with open(filepath, 'r') as f:
        c = f.read()
    c = c.replace("androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack", "androidx.compose.material.icons.automirrored.filled.ArrowBack")
    if "import androidx.compose.material.icons.automirrored.filled.ArrowBack" not in c:
        c = c.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.automirrored.filled.ArrowBack")
    with open(filepath, 'w') as f:
        f.write(c)

fix_arrowback('app/src/main/java/com/example/ui/screens/MiniGames.kt')
fix_arrowback('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt')
