/*
LeetCode 70
Climbing Stairs

Difficulty: Easy

Approach:
Dynamic programming (Fibonacci-like). Ways to reach step n equals the sum
of ways to reach step n-1 and n-2. Use two rolling variables instead of
a full array for O(1) space.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int prev2 = 1, prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
}
