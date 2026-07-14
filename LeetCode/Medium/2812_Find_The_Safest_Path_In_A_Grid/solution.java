/*
LeetCode 2812
Find the Safest Path in a Grid

Difficulty: Medium

Approach:
Multi-source BFS from all thieves to compute safety scores for each cell.
Binary search on the answer: for each candidate safety value, check if a
path exists from (0,0) to (n-1,n-1) using only cells with safety >= mid.

Time Complexity: O(n^2 * log n)
Space Complexity: O(n^2)
*/

import java.util.*;

class Solution {
    private static final int[][] DIRS = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    public int maximumSafenessFactor(List<List<Integer>> grid) {
        int n = grid.size();
        if (grid.get(0).get(0) == 1 || grid.get(n - 1).get(n - 1) == 1) return 0;

        int[][] safety = new int[n][n];
        Queue<int[]> queue = new LinkedList<>();

        for (int[] row : safety) Arrays.fill(row, Integer.MAX_VALUE);
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                if (grid.get(r).get(c) == 1) {
                    safety[r][c] = 0;
                    queue.offer(new int[]{r, c});
                }
            }
        }

        while (!queue.isEmpty()) {
            int[] cell = queue.poll();
            for (int[] d : DIRS) {
                int nr = cell[0] + d[0], nc = cell[1] + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && safety[nr][nc] > safety[cell[0]][cell[1]] + 1) {
                    safety[nr][nc] = safety[cell[0]][cell[1]] + 1;
                    queue.offer(new int[]{nr, nc});
                }
            }
        }

        int low = 0, high = 2 * n, result = 0;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (canReach(safety, n, mid)) {
                result = mid;
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result;
    }

    private boolean canReach(int[][] safety, int n, int minSafety) {
        if (safety[0][0] < minSafety) return false;
        boolean[][] visited = new boolean[n][n];
        visited[0][0] = true;
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0});
        while (!queue.isEmpty()) {
            int[] cell = queue.poll();
            if (cell[0] == n - 1 && cell[1] == n - 1) return true;
            for (int[] d : DIRS) {
                int nr = cell[0] + d[0], nc = cell[1] + d[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && !visited[nr][nc] && safety[nr][nc] >= minSafety) {
                    visited[nr][nc] = true;
                    queue.offer(new int[]{nr, nc});
                }
            }
        }
        return false;
    }
}
