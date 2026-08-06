import os

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    wallet = f.read()
if "import androidx.compose.material3.MenuAnchorType" not in wallet:
    wallet = wallet.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\nimport androidx.compose.material3.MenuAnchorType")
with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(wallet)


def add_imports(filepath):
    with open(filepath, 'r') as f:
        c = f.read()
    if "import androidx.compose.material.icons.Icons" not in c:
        c = c.replace("import androidx.compose.material.icons.filled.PlayArrow", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.automirrored.filled.ArrowBack\nimport androidx.compose.material.icons.filled.PlayArrow")
    with open(filepath, 'w') as f:
        f.write(c)

add_imports('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt')
add_imports('app/src/main/java/com/example/ui/screens/MiniGames.kt')
