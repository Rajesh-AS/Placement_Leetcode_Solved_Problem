"""
LeetCode 704
Binary Search

Difficulty: Easy

Approach:
Classic binary search. Maintain left and right pointers. Compute mid,
compare nums[mid] with target. Narrow the search space by half each
iteration. Return mid if found, else return -1.

Time Complexity: O(log n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
