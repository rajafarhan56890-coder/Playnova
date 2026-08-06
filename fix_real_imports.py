import os

def fix_imports(filepath):
    with open(filepath, 'r') as f:
        c = f.read()
    c = c.replace("import Icons.AutoMirrored.Filled.ArrowBack", "import androidx.compose.material.icons.automirrored.filled.ArrowBack")
    if "import androidx.compose.material.icons.Icons" not in c:
        c = c.replace("import androidx.compose.material.icons.automirrored.filled.ArrowBack", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.automirrored.filled.ArrowBack")
    with open(filepath, 'w') as f:
        f.write(c)

fix_imports('app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt')
fix_imports('app/src/main/java/com/example/ui/screens/MiniGames.kt')

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    w = f.read()
w = w.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\nimport androidx.compose.material3.MenuAnchorType")
with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(w)
