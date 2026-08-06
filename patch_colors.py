import os

color_kt = """package com.example.ui.theme

import androidx.compose.ui.graphics.Color

val BrandPrimary = Color(0xFF6366F1) // Indigo 500
val BrandSecondary = Color(0xFF10B981) // Emerald 500
val BrandTertiary = Color(0xFFF59E0B) // Amber 500

val LightBackground = Color(0xFFF9FAFB) // Gray 50
val LightSurface = Color(0xFFFFFFFF) // White
val LightSurfaceVariant = Color(0xFFF3F4F6) // Gray 100
val LightOnBackground = Color(0xFF111827) // Gray 900
val LightOnSurfaceVariant = Color(0xFF4B5563) // Gray 600

val DarkBackground = Color(0xFF111827) // Gray 900
val DarkSurface = Color(0xFF1F2937) // Gray 800
val DarkSurfaceVariant = Color(0xFF374151) // Gray 700
val DarkOnBackground = Color(0xFFF9FAFB) // Gray 50
val DarkOnSurfaceVariant = Color(0xFF9CA3AF) // Gray 400

val GoldAccent = Color(0xFFF59E0B)
"""
with open('app/src/main/java/com/example/ui/theme/Color.kt', 'w') as f:
    f.write(color_kt)

theme_kt = """package com.example.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = BrandPrimary,
    secondary = BrandSecondary,
    tertiary = BrandTertiary,
    background = DarkBackground,
    surface = DarkSurface,
    onPrimary = Color.White,
    onSecondary = Color.White,
    onTertiary = Color.White,
    onBackground = DarkOnBackground,
    onSurface = DarkOnBackground,
    surfaceVariant = DarkSurfaceVariant,
    onSurfaceVariant = DarkOnSurfaceVariant,
    primaryContainer = BrandPrimary.copy(alpha = 0.2f),
    onPrimaryContainer = BrandPrimary,
    secondaryContainer = BrandSecondary.copy(alpha = 0.2f),
    onSecondaryContainer = BrandSecondary,
    tertiaryContainer = BrandTertiary.copy(alpha = 0.2f),
    onTertiaryContainer = BrandTertiary
)

private val LightColorScheme = lightColorScheme(
    primary = BrandPrimary,
    secondary = BrandSecondary,
    tertiary = BrandTertiary,
    background = LightBackground,
    surface = LightSurface,
    onPrimary = Color.White,
    onSecondary = Color.White,
    onTertiary = Color.White,
    onBackground = LightOnBackground,
    onSurface = LightOnBackground,
    surfaceVariant = LightSurfaceVariant,
    onSurfaceVariant = LightOnSurfaceVariant,
    primaryContainer = BrandPrimary.copy(alpha = 0.1f),
    onPrimaryContainer = BrandPrimary,
    secondaryContainer = BrandSecondary.copy(alpha = 0.1f),
    onSecondaryContainer = BrandSecondary,
    tertiaryContainer = BrandTertiary.copy(alpha = 0.1f),
    onTertiaryContainer = BrandTertiary
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }
    MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
"""
with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(theme_kt)
