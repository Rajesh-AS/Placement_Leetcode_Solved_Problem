/*
LeetCode 3402
Minimum Operations to Make Columns Strictly Increasing

Difficulty: Easy

Approach:
For each column, iterate top to bottom. If the current element is not
strictly greater than the previous, increase it to previous + 1 and
add the difference to operations count.

Time Complexity: O(m * n)
Space Complexity: O(1)
*/

class Solution {
    public int minimumOperations(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int operations = 0;
        for (int col = 0; col < n; col++) {
            int prev = grid[0][col];
            for (int row = 1; row < m; row++) {
                if (grid[row][col] <= prev) {
                    operations += prev + 1 - grid[row][col];
                    prev = prev + 1;
                } else {
                    prev = grid[row][col];
                }
            }
        }
        return operations;
    }
}
