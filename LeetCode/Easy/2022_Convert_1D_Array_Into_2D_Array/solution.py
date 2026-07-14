"""
LeetCode 2022
Convert 1D Array Into 2D Array

Difficulty: Easy

Approach:
Check if m * n equals the original array length. If not, return [].
Otherwise, slice the array into chunks of size n to form each row
of the 2D array.

Time Complexity: O(m * n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if m * n != len(original):
            return []
        return [original[i * n:(i + 1) * n] for i in range(m)]
