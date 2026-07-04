"""
LeetCode 3402
Minimum Operations to Make Columns Strictly Increasing

Difficulty: Easy

Approach:
For each column, iterate top to bottom. If the current element is not
strictly greater than the previous, increase it to previous + 1 and
add the difference to operations count.

Time Complexity: O(m * n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def minimumOperations(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        operations = 0
        for col in range(n):
            prev = grid[0][col]
            for row in range(1, m):
                if grid[row][col] <= prev:
                    operations += prev + 1 - grid[row][col]
                    prev = prev + 1
                else:
                    prev = grid[row][col]
        return operations
