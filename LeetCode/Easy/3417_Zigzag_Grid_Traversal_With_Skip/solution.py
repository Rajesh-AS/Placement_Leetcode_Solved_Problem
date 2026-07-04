"""
LeetCode 3417
Zigzag Grid Traversal With Skip

Difficulty: Easy

Approach:
Traverse the grid in zigzag order (even rows left-to-right, odd rows
right-to-left). Maintain a boolean toggle to skip every other element
across the entire zigzag sequence. Collect non-skipped elements.

Time Complexity: O(m * n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def zigzagTraversal(self, grid: List[List[int]]) -> List[int]:
        result = []
        pick = True
        for i, row in enumerate(grid):
            order = row if i % 2 == 0 else row[::-1]
            for val in order:
                if pick:
                    result.append(val)
                pick = not pick
        return result
