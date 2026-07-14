/*
LeetCode 3286
Find a Safe Walk Through a Grid

Difficulty: Medium

Approach:
0-1 BFS using a deque. Each cell costs grid[r][c] (0 or 1). Find the
minimum cost path from (0,0) to (m-1,n-1). If the total cost including
start cell is less than health, return true.

Time Complexity: O(m * n)
Space Complexity: O(m * n)
*/

import java.util.*;

class Solution {
    public boolean findSafeWalk(List<List<Integer>> grid, int health) {
        int m = grid.size(), n = grid.get(0).size();
        int[][] dist = new int[m][n];
        for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE);
        dist[0][0] = grid.get(0).get(0);
        Deque<int[]> deque = new ArrayDeque<>();
        deque.offerFirst(new int[]{0, 0});
        int[][] dirs = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

        while (!deque.isEmpty()) {
            int[] cell = deque.pollFirst();
            int r = cell[0], c = cell[1];
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                    int newDist = dist[r][c] + grid.get(nr).get(nc);
                    if (newDist < dist[nr][nc]) {
                        dist[nr][nc] = newDist;
                        if (grid.get(nr).get(nc) == 0) {
                            deque.offerFirst(new int[]{nr, nc});
                        } else {
                            deque.offerLast(new int[]{nr, nc});
                        }
                    }
                }
            }
        }
        return dist[m - 1][n - 1] < health;
    }
}
