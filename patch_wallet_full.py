import os
import re

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'r') as f:
    content = f.read()

# Make the TransactionItemDetailed much cleaner
old_tx = """@Composable
fun TransactionItemDetailed(title: String, amount: String, isPositive: Boolean, date: Date, status: String) {
    val formatter = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(RoundedCornerShape(20.dp))
                    .background(
                        if (isPositive) MaterialTheme.colorScheme.secondary.copy(alpha = 0.2f)
                        else MaterialTheme.colorScheme.tertiary.copy(alpha = 0.2f)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (isPositive) Icons.Default.ArrowDownward else Icons.Default.ArrowUpward,
                    contentDescription = null,
                    tint = if (isPositive) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.tertiary
                )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = title,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Text(
                    text = "${formatter.format(date)} • ${status.capitalize()}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                )
            }
        }
        Text(
            text = amount,
            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
            color = if (isPositive) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.tertiary
        )
    }
}"""

new_tx = """@Composable
fun TransactionItemDetailed(title: String, amount: String, isPositive: Boolean, date: Date, status: String) {
    val formatter = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp)
            .clip(RoundedCornerShape(20.dp))
            .background(MaterialTheme.colorScheme.surface)
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(
                        if (isPositive) MaterialTheme.colorScheme.secondary.copy(alpha = 0.15f)
                        else MaterialTheme.colorScheme.error.copy(alpha = 0.15f)
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = if (isPositive) Icons.Default.ArrowDownward else Icons.Default.ArrowUpward,
                    contentDescription = null,
                    tint = if (isPositive) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.error
                )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onBackground
                )
                Text(
                    text = "${formatter.format(date)} • ${status.replaceFirstChar { if (it.isLowerCase()) it.titlecase(Locale.getDefault()) else it.toString() }}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        Text(
            text = amount,
            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Black),
            color = if (isPositive) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.error
        )
    }
}"""

# Fix deprecations in WalletScreen too
content = content.replace("Icons.Default.ArrowBack", "Icons.AutoMirrored.Filled.ArrowBack")
content = content.replace(old_tx, new_tx)

with open('app/src/main/java/com/example/ui/screens/WalletScreen.kt', 'w') as f:
    f.write(content)
