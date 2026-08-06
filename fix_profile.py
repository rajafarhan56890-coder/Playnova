import os

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

if "import androidx.compose.ui.platform.LocalClipboardManager" not in content:
    content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.platform.LocalClipboardManager\nimport androidx.compose.ui.text.AnnotatedString")
    content = content.replace("import androidx.compose.material.icons.filled.GroupAdd", "import androidx.compose.material.icons.filled.GroupAdd\nimport androidx.compose.material.icons.filled.ContentCopy\nimport androidx.compose.material.icons.filled.Share")
    content = content.replace("import androidx.compose.material3.Button", "import androidx.compose.material3.Button\nimport androidx.compose.material3.IconButton\nimport android.content.Intent\nimport androidx.compose.ui.platform.LocalContext\nimport android.widget.Toast")

old_ref = """                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(MaterialTheme.colorScheme.background)
                        .padding(16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = user?.referralCode ?: "NOVA-X79B",
                        style = MaterialTheme.typography.headlineSmall.copy(fontWeight = FontWeight.Bold),
                        color = MaterialTheme.colorScheme.primary
                    )
                }"""

new_ref = """                val clipboardManager = LocalClipboardManager.current
                val context = LocalContext.current
                val refCode = user?.referralCode ?: "NOVA-X79B"
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(MaterialTheme.colorScheme.background)
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = refCode,
                        style = MaterialTheme.typography.headlineSmall.copy(fontWeight = FontWeight.Bold),
                        color = MaterialTheme.colorScheme.primary
                    )
                    Row {
                        IconButton(onClick = {
                            clipboardManager.setText(AnnotatedString(refCode))
                            Toast.makeText(context, "Copied to clipboard", Toast.LENGTH_SHORT).show()
                        }) {
                            Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                        }
                        IconButton(onClick = {
                            val sendIntent = Intent(Intent.ACTION_SEND).apply {
                                putExtra(Intent.EXTRA_TEXT, "Join Pinjoy and earn rewards! Use my referral code: $refCode")
                                type = "text/plain"
                            }
                            val shareIntent = Intent.createChooser(sendIntent, null)
                            context.startActivity(shareIntent)
                        }) {
                            Icon(Icons.Default.Share, contentDescription = "Share")
                        }
                    }
                }"""

content = content.replace(old_ref, new_ref)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
