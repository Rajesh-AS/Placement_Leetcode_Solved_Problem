"""
LeetCode 3286
Find a Safe Walk Through a Grid

Difficulty: Medium

Approach:
0-1 BFS using a deque. Each cell costs grid[r][c] (0 or 1). Find the
minimum cost path from (0,0) to (m-1,n-1). If the total cost including
start cell is less than health, return True.

Time Complexity: O(m * n)
Space Complexity: O(m * n)
"""

from typing import List
from collections import deque


class Solution:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m, n = len(grid), len(grid[0])
        dist = [[float('inf')] * n for _ in range(m)]
        dist[0][0] = grid[0][0]
        dq = deque([(0, 0)])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while dq:
            r, c = dq.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    new_dist = dist[r][c] + grid[nr][nc]
                    if new_dist < dist[nr][nc]:
                        dist[nr][nc] = new_dist
                        if grid[nr][nc] == 0:
                            dq.appendleft((nr, nc))
                        else:
                            dq.append((nr, nc))

        return dist[m - 1][n - 1] < health
