/*
LeetCode 1486
XOR Operation in an Array

Difficulty: Easy

Approach:
Compute nums[i] = start + 2 * i for each index i from 0 to n-1.
XOR all elements together using a running XOR variable.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int xorOperation(int n, int start) {
        int result = 0;
        for (int i = 0; i < n; i++) {
            result ^= start + 2 * i;
        }
        return result;
    }
}
