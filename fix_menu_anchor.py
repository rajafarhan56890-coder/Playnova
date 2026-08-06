import os

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("modifier = Modifier.menuAnchor()", "modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable)")
content = content.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\nimport androidx.compose.material3.MenuAnchorType")

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(content)
