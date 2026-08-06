import os

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    w = f.read()
if "import androidx.compose.material3.MenuAnchorType" not in w:
    w = w.replace("import androidx.compose.material3.ExperimentalMaterial3Api", "import androidx.compose.material3.ExperimentalMaterial3Api\nimport androidx.compose.material3.MenuAnchorType")
with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(w)
