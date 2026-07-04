/*
LeetCode 3417
Zigzag Grid Traversal With Skip

Difficulty: Easy

Approach:
Traverse the grid in zigzag order (even rows left-to-right, odd rows
right-to-left). Maintain a boolean toggle to skip every other element
across the entire zigzag sequence. Collect non-skipped elements.

Time Complexity: O(m * n)
Space Complexity: O(1)
*/

import java.util.*;

class Solution {
    public List<Integer> zigzagTraversal(int[][] grid) {
        List<Integer> result = new ArrayList<>();
        boolean pick = true;
        for (int i = 0; i < grid.length; i++) {
            if (i % 2 == 0) {
                for (int j = 0; j < grid[i].length; j++) {
                    if (pick) result.add(grid[i][j]);
                    pick = !pick;
                }
            } else {
                for (int j = grid[i].length - 1; j >= 0; j--) {
                    if (pick) result.add(grid[i][j]);
                    pick = !pick;
                }
            }
        }
        return result;
    }
}
