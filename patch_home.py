import os

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.animation.animateContentSize" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.animation.animateContentSize")

old_lazycolumn = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(padding),
            contentPadding = PaddingValues(bottom = 100.dp)
        ) {"""

new_lazycolumn = """        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .padding(padding)
                .animateContentSize(),
            contentPadding = PaddingValues(bottom = 100.dp)
        ) {"""
content = content.replace(old_lazycolumn, new_lazycolumn)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
