# LeetCode 3286 - Find a Safe Walk Through a Grid

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/find-a-safe-walk-through-a-grid/](https://leetcode.com/problems/find-a-safe-walk-through-a-grid/)

## Approach

Use **0-1 BFS** (BFS with a deque). Each cell has a cost equal to `grid[r][c]` (0 or 1). Find the minimum cost path from `(0,0)` to `(m-1,n-1)`. If the minimum total cost (including the starting cell) is less than `health`, the walk is safe. Push 0-cost edges to the front and 1-cost edges to the back of the deque.

## Time Complexity

O(m × n) — each cell is visited at most once.

## Space Complexity

O(m × n) — for the distance grid and deque.
