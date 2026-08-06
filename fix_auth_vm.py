with open('app/src/main/java/com/example/ui/viewmodels/AuthViewModel.kt', 'r') as f:
    content = f.read()

# Find the last two closing braces and the appended method
last_brace_idx = content.rfind('}')
second_last_brace_idx = content.rfind('}', 0, last_brace_idx)

# Wait, the end of the original file was:
#    private fun generateReferralCode(): String {
#        return "NOVA-" + UUID.randomUUID().toString().substring(0, 5).uppercase()
#    }
#}
#    fun addBalance(amount: Long, title: String) {
#...

import re
content = re.sub(r'    }\n}\n    fun addBalance', '    }\n    fun addBalance', content)
content += "\n}\n"

with open('app/src/main/java/com/example/ui/viewmodels/AuthViewModel.kt', 'w') as f:
    f.write(content)
