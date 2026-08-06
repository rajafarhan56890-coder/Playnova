import os

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.animation.animateContentSize" not in content:
    content = content.replace("import androidx.compose.animation.AnimatedVisibility", "import androidx.compose.animation.AnimatedVisibility\nimport androidx.compose.animation.animateContentSize")

old_col = """    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),"""

new_col = """    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .animateContentSize(),"""

content = content.replace(old_col, new_col)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)
