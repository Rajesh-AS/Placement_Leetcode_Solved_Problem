"""
LeetCode 628
Maximum Product of Three Numbers

Difficulty: Easy

Approach:
Sort the array. The max product is either the product of the three largest
numbers or the product of the two smallest (negative) numbers and the
largest number. Return the maximum of both candidates.

Time Complexity: O(n log n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def maximumProduct(self, nums: List[int]) -> int:
        nums.sort()
        return max(
            nums[-1] * nums[-2] * nums[-3],
            nums[0] * nums[1] * nums[-1]
        )
