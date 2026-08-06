import os

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    c = f.read()

if "import androidx.compose.foundation.layout.Arrangement" not in c:
    c = c.replace("import androidx.compose.foundation.layout.Box", "import androidx.compose.foundation.layout.Box\nimport androidx.compose.foundation.layout.Arrangement")
with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(c)

