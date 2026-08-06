import re
with open('app/src/main/java/com/example/ui/screens/MiniGames.kt', 'r') as f:
    content = f.read()

content = content.replace('"4" -> ColorMatchGame(onReward = { onReward(it.toLong()); onBack() })', '"4" -> ColorMatchGame(onReward = { onReward(it.toLong()); onBack() })\n                "5" -> FlappyBirdGame(onReward = { onReward(it.toLong()); onBack() })')

content = content.replace('"4" -> "Color Match"', '"4" -> "Color Match"\n        "5" -> "Flappy Nova"')

with open('app/src/main/java/com/example/ui/screens/MiniGames.kt', 'w') as f:
    f.write(content)
