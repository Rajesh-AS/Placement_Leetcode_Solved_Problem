"""
LeetCode 1480
Running Sum of 1d Array

Difficulty: Easy

Approach:
Iterate from index 1, adding the previous element to the current one.
This builds the prefix sum array in-place.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]
        return nums
