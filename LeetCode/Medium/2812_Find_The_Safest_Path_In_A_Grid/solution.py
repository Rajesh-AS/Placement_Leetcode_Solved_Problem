"""
LeetCode 2812
Find the Safest Path in a Grid

Difficulty: Medium

Approach:
Multi-source BFS from all thieves to compute safety scores for each cell.
Binary search on the answer: for each candidate safety value, check if a
path exists from (0,0) to (n-1,n-1) using only cells with safety >= mid.

Time Complexity: O(n^2 * log n)
Space Complexity: O(n^2)
"""

from typing import List
from collections import deque


class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
            return 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        safety = [[0] * n for _ in range(n)]
        queue = deque()

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    queue.append((r, c))
                    safety[r][c] = 0
                else:
                    safety[r][c] = float('inf')

        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and safety[nr][nc] > safety[r][c] + 1:
                    safety[nr][nc] = safety[r][c] + 1
                    queue.append((nr, nc))

        def can_reach(min_safety):
            if safety[0][0] < min_safety:
                return False
            visited = [[False] * n for _ in range(n)]
            visited[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == n - 1 and c == n - 1:
                    return True
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and safety[nr][nc] >= min_safety:
                        visited[nr][nc] = True
                        q.append((nr, nc))
            return False

        low, high = 0, n * 2
        result = 0
        while low <= high:
            mid = (low + high) // 2
            if can_reach(mid):
                result = mid
                low = mid + 1
            else:
                high = mid - 1
        return result
