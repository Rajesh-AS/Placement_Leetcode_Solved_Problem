"""
LeetCode 69
Sqrt(x)

Difficulty: Easy

Approach:
Binary search in range [0, x]. Find the largest mid where mid * mid <= x.
This gives the integer (floor) square root.

Time Complexity: O(log x)
Space Complexity: O(1)
"""


class Solution:
    def mySqrt(self, x: int) -> int:
        left, right = 0, x
        result = 0
        while left <= right:
            mid = left + (right - left) // 2
            if mid * mid <= x:
                result = mid
                left = mid + 1
            else:
                right = mid - 1
        return result
