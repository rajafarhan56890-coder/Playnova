with open('app/src/main/java/com/example/ui/screens/MiniGames.kt', 'r') as f:
    content = f.read()

old_draw = """                androidx.compose.ui.graphics.drawscope.drawIntoCanvas {
                    // Top pipe
                    drawRect(Color.Green, topLeft = androidx.compose.ui.geometry.Offset(pipeLeft, 0f), size = androidx.compose.ui.geometry.Size(pipeWidth * canvasWidth, gapTop))
                    // Bottom pipe
                    drawRect(Color.Green, topLeft = androidx.compose.ui.geometry.Offset(pipeLeft, gapBottom), size = androidx.compose.ui.geometry.Size(pipeWidth * canvasWidth, canvasHeight - gapBottom))
                }"""

new_draw = """                // Top pipe
                drawRect(Color.Green, topLeft = androidx.compose.ui.geometry.Offset(pipeLeft, 0f), size = androidx.compose.ui.geometry.Size(pipeWidth * canvasWidth, gapTop))
                // Bottom pipe
                drawRect(Color.Green, topLeft = androidx.compose.ui.geometry.Offset(pipeLeft, gapBottom), size = androidx.compose.ui.geometry.Size(pipeWidth * canvasWidth, canvasHeight - gapBottom))"""

content = content.replace(old_draw, new_draw)

with open('app/src/main/java/com/example/ui/screens/MiniGames.kt', 'w') as f:
    f.write(content)
