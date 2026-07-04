# LeetCode 999 - Available Captures for Rook

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/available-captures-for-rook/](https://leetcode.com/problems/available-captures-for-rook/)

## Approach

Find the rook (`R`) position on the 8×8 board. From the rook's position, scan in all four cardinal directions (up, down, left, right). In each direction, stop at the first piece encountered — if it's a pawn (`p`), increment the capture count; if it's a bishop (`B`), stop without capturing.

## Time Complexity

O(1) — the board is always 8×8, so all operations are constant.

## Space Complexity

O(1) — no extra space used.
