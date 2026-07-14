# LeetCode 2812 - Find the Safest Path in a Grid

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/find-the-safest-path-in-a-grid/](https://leetcode.com/problems/find-the-safest-path-in-a-grid/)

## Approach

1. **Multi-source BFS**: Run BFS from all thief cells simultaneously to compute the safety factor (minimum Manhattan distance to any thief) for every cell in the grid.
2. **Binary search on the answer**: Binary search on the minimum safety value `mid`. For each candidate, check if there exists a path from `(0,0)` to `(n-1,n-1)` using only cells with safety ≥ `mid` (verified via BFS/DFS).
3. Return the largest feasible `mid`.

## Time Complexity

O(n² log n) — BFS is O(n²) and binary search adds a log n factor.

## Space Complexity

O(n²) — for the safety grid and visited arrays.
