"""
LeetCode 999
Available Captures for Rook

Difficulty: Easy

Approach:
Find the rook position. Scan in four cardinal directions. In each
direction, stop at the first piece: if it's a pawn ('p'), count it
as a capture; if it's a bishop ('B'), stop without capturing.

Time Complexity: O(1)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def numRookCaptures(self, board: List[List[str]]) -> int:
        rook_row, rook_col = 0, 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == 'R':
                    rook_row, rook_col = r, c

        captures = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = rook_row + dr, rook_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] == 'B':
                    break
                if board[r][c] == 'p':
                    captures += 1
                    break
                r += dr
                c += dc
        return captures
