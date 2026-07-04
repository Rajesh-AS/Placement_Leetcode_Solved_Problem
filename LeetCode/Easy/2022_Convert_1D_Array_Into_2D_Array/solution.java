/*
LeetCode 2022
Convert 1D Array Into 2D Array

Difficulty: Easy

Approach:
Check if m * n equals the original array length. If not, return empty.
Otherwise, fill the 2D array row by row using an index pointer.

Time Complexity: O(m * n)
Space Complexity: O(1)
*/

class Solution {
    public int[][] construct2DArray(int[] original, int m, int n) {
        if (m * n != original.length) return new int[0][];
        int[][] result = new int[m][n];
        for (int i = 0; i < original.length; i++) {
            result[i / n][i % n] = original[i];
        }
        return result;
    }
}
