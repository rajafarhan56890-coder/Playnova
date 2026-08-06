import os

files_to_fix = [
    'app/src/main/java/com/example/ui/screens/MiniGames.kt',
    'app/src/main/java/com/example/ui/screens/GameDetailsScreen.kt'
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        content = content.replace("Icons.Default.ArrowBack", "androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack")
        content = content.replace("import androidx.compose.material.icons.filled.ArrowBack\n", "")
        
        with open(file_path, 'w') as f:
            f.write(content)
