"""
LeetCode 67
Add Binary

Difficulty: Easy

Approach:
Iterate from the rightmost digits of both strings. Add corresponding
digits with carry. Append sum % 2 to result, update carry to sum // 2.
Reverse the result string at the end.

Time Complexity: O(max(m, n))
Space Complexity: O(max(m, n))
"""


class Solution:
    def addBinary(self, a: str, b: str) -> str:
        result = []
        carry = 0
        i, j = len(a) - 1, len(b) - 1
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += int(a[i])
                i -= 1
            if j >= 0:
                total += int(b[j])
                j -= 1
            result.append(str(total % 2))
            carry = total // 2
        return ''.join(reversed(result))
