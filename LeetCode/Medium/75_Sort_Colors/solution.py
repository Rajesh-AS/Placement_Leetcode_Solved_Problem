"""
LeetCode 75
Sort Colors

Difficulty: Medium

Approach:
Dutch National Flag algorithm. Use three pointers: low, mid, high.
Swap 0s to the front and 2s to the back in a single pass, leaving
1s in the middle. This sorts the array in-place.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def sortColors(self, nums: List[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
