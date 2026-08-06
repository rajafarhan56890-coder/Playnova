import os

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

old_header = """        // Profile Header
        Box(
            modifier = Modifier
                .size(100.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center
        ) {
            if (user?.profileImageUrl != null) {
                AsyncImage(
                    model = user.profileImageUrl,
                    contentDescription = "Profile Image",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            } else {
                Text(
                    text = user?.username?.firstOrNull()?.toString()?.uppercase() ?: "P",
                    style = MaterialTheme.typography.displayMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = user?.username ?: "PlayerOne",
            style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
            color = MaterialTheme.colorScheme.onBackground
        )
        Text(
            text = user?.email ?: "playerone@example.com",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f)
        )"""

new_header = """        // Profile Header
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(32.dp))
                .background(
                    androidx.compose.ui.graphics.Brush.verticalGradient(
                        colors = listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.secondary)
                    )
                )
                .padding(32.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Box(
                    modifier = Modifier
                        .size(100.dp)
                        .clip(CircleShape)
                        .background(Color.White),
                    contentAlignment = Alignment.Center
                ) {
                    if (user?.profileImageUrl != null) {
                        AsyncImage(
                            model = user.profileImageUrl,
                            contentDescription = "Profile Image",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop
                        )
                    } else {
                        Text(
                            text = user?.username?.firstOrNull()?.toString()?.uppercase() ?: "P",
                            style = MaterialTheme.typography.displayMedium,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = user?.username ?: "PlayerOne",
                    style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                    color = Color.White
                )
                Text(
                    text = user?.email ?: "playerone@example.com",
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color.White.copy(alpha = 0.8f)
                )
            }
        }"""

content = content.replace(old_header, new_header)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
