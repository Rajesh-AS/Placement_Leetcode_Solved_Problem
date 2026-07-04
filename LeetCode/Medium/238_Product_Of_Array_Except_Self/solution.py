"""
LeetCode 238
Product of Array Except Self

Difficulty: Medium

Approach:
Two-pass approach without division. First pass builds prefix products
from left to right. Second pass multiplies a running suffix product
from right to left. Each position ends up with the product of all
elements except itself.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]
        return result
