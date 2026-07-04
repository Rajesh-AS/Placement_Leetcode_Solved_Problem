"""
LeetCode 70
Climbing Stairs

Difficulty: Easy

Approach:
Dynamic programming (Fibonacci-like). Ways to reach step n equals the sum
of ways to reach step n-1 and n-2. Use two rolling variables instead of
a full array for O(1) space.

Time Complexity: O(n)
Space Complexity: O(1)
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            prev2, prev1 = prev1, prev1 + prev2
        return prev1
