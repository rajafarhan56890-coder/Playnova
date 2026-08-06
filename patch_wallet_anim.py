import os

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.animation.animateContentSize" not in content:
    content = content.replace("import androidx.compose.animation.AnimatedContent", "import androidx.compose.animation.AnimatedContent\nimport androidx.compose.animation.animateContentSize")

old_lazy = """    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),"""

new_lazy = """    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .animateContentSize(),"""

content = content.replace(old_lazy, new_lazy)

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(content)
