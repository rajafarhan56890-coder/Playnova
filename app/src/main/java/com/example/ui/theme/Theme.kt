package com.example.ui.theme

import android.app.Activity
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme =
  darkColorScheme(
    primary = NovaPrimary,
    secondary = NovaSecondary,
    tertiary = NovaTertiary,
    background = NovaBackground,
    surface = NovaSurface,
    onPrimary = NovaOnPrimary,
    onSecondary = NovaBackground,
    onTertiary = NovaOnPrimary,
    onBackground = NovaOnBackground,
    onSurface = NovaOnSurface,
    error = NovaError,
    surfaceVariant = Color(0xFF261D42)
  )

@Composable
fun MyApplicationTheme(
  content: @Composable () -> Unit,
) {
  val colorScheme = DarkColorScheme
  val view = LocalView.current
  if (!view.isInEditMode) {
    SideEffect {
      val window = (view.context as Activity).window
      WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
    }
  }

  MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
