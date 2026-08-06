import os

color_kt = """package com.example.ui.theme

import androidx.compose.ui.graphics.Color

val NovaPrimary = Color(0xFF6C5CE7) // Deep Purple / Periwinkle
val NovaSecondary = Color(0xFF00CEC9) // Teal
val NovaTertiary = Color(0xFFFD79A8) // Pink
val NovaBackground = Color(0xFFF8F9FA) // Light mode background
val NovaSurface = Color(0xFFFFFFFF) // Light mode surface
val NovaOnPrimary = Color(0xFFFFFFFF)
val NovaOnBackground = Color(0xFF2D3436)
val NovaOnSurface = Color(0xFF2D3436)
val NovaError = Color(0xFFD63031)

val NovaDarkBackground = Color(0xFF0F0E17)
val NovaDarkSurface = Color(0xFF16161A)
val NovaDarkOnBackground = Color(0xFFFFFFFE)
val NovaDarkOnSurface = Color(0xFF94A1B2)

val GoldAccent = Color(0xFFFFC312)
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
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = NovaPrimary,
    secondary = NovaSecondary,
    tertiary = NovaTertiary,
    background = NovaDarkBackground,
    surface = NovaDarkSurface,
    onPrimary = NovaOnPrimary,
    onSecondary = Color.Black,
    onTertiary = NovaOnPrimary,
    onBackground = NovaDarkOnBackground,
    onSurface = NovaDarkOnSurface,
    error = NovaError,
    surfaceVariant = Color(0xFF242629),
    onSurfaceVariant = Color(0xFF94A1B2),
    primaryContainer = Color(0xFF6C5CE7).copy(alpha = 0.2f),
    onPrimaryContainer = Color(0xFFE2DDF8),
    tertiaryContainer = Color(0xFFFD79A8).copy(alpha = 0.2f),
    onTertiaryContainer = Color(0xFFFD79A8)
)

private val LightColorScheme = lightColorScheme(
    primary = NovaPrimary,
    secondary = NovaSecondary,
    tertiary = NovaTertiary,
    background = NovaBackground,
    surface = NovaSurface,
    onPrimary = NovaOnPrimary,
    onSecondary = Color.White,
    onTertiary = NovaOnPrimary,
    onBackground = NovaOnBackground,
    onSurface = NovaOnSurface,
    error = NovaError,
    surfaceVariant = Color(0xFFF1F3F5),
    onSurfaceVariant = Color(0xFF495057),
    primaryContainer = Color(0xFFE5E0FA),
    onPrimaryContainer = Color(0xFF6C5CE7),
    tertiaryContainer = Color(0xFFFFE3EE),
    onTertiaryContainer = Color(0xFFFD79A8)
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

type_kt = """package com.example.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Black,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Bold,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp
    ),
    headlineLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Bold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp
    ),
    labelLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Bold,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    )
)
"""

with open('app/src/main/java/com/example/ui/theme/Type.kt', 'w') as f:
    f.write(type_kt)

