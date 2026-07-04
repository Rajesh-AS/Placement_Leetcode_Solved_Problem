"""
LeetCode 747
Largest Number At Least Twice of Others

Difficulty: Easy

Approach:
Find the maximum and second maximum in a single pass. If the maximum
is at least twice the second maximum, return its index. Otherwise
return -1.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def dominantIndex(self, nums: List[int]) -> int:
        max_val = max(nums)
        max_idx = nums.index(max_val)
        for i, num in enumerate(nums):
            if i != max_idx and max_val < 2 * num:
                return -1
        return max_idx
