sed -i '328,$d' app/src/main/java/com/example/ui/screens/HomeScreen.kt
cat << 'INNER_EOF' >> app/src/main/java/com/example/ui/screens/HomeScreen.kt

@Composable
fun TrendChartCard(currentBalance: Long) {
    val trendData = remember(currentBalance) {
        val data = mutableListOf<Float>()
        var current = currentBalance.toFloat()
        data.add(current)
        for (i in 0..5) {
            current = (current - (10..100).random()).coerceAtLeast(0f)
            data.add(current)
        }
        data.reversed()
    }

    Card(
        modifier = Modifier.fillMaxWidth().height(180.dp),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Text(
                text = "7-Day Trend",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurface
            )
            Spacer(modifier = Modifier.height(16.dp))
            val lineColor = MaterialTheme.colorScheme.secondary
            androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                val max = trendData.maxOrNull() ?: 100f
                val min = trendData.minOrNull() ?: 0f
                val range = (max - min).coerceAtLeast(1f)
                
                val width = size.width
                val height = size.height
                val stepX = width / (trendData.size - 1)
                
                val path = androidx.compose.ui.graphics.Path()
                val fillPath = androidx.compose.ui.graphics.Path()
                
                trendData.forEachIndexed { index, value ->
                    val x = index * stepX
                    val y = height - ((value - min) / range * height)
                    if (index == 0) {
                        path.moveTo(x, y)
                        fillPath.moveTo(x, height)
                        fillPath.lineTo(x, y)
                    } else {
                        path.lineTo(x, y)
                        fillPath.lineTo(x, y)
                    }
                    if (index == trendData.size - 1) {
                        fillPath.lineTo(x, height)
                        fillPath.close()
                    }
                }
                
                drawPath(
                    path = fillPath,
                    brush = androidx.compose.ui.graphics.Brush.verticalGradient(
                        colors = listOf(
                            lineColor.copy(alpha = 0.3f),
                            androidx.compose.ui.graphics.Color.Transparent
                        )
                    )
                )
                
                drawPath(
                    path = path,
                    color = lineColor,
                    style = androidx.compose.ui.graphics.drawscope.Stroke(
                        width = 4.dp.toPx(),
                        cap = androidx.compose.ui.graphics.StrokeCap.Round,
                        join = androidx.compose.ui.graphics.StrokeJoin.Round
                    )
                )
                
                trendData.forEachIndexed { index, value ->
                    val x = index * stepX
                    val y = height - ((value - min) / range * height)
                    drawCircle(
                        color = lineColor,
                        radius = 6.dp.toPx(),
                        center = androidx.compose.ui.geometry.Offset(x, y)
                    )
                    drawCircle(
                        color = androidx.compose.ui.graphics.Color.White,
                        radius = 3.dp.toPx(),
                        center = androidx.compose.ui.geometry.Offset(x, y)
                    )
                }
            }
        }
    }
}
INNER_EOF
