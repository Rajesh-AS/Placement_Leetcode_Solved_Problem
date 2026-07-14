/*
LeetCode 1672
Richest Customer Wealth

Difficulty: Easy

Approach:
For each customer, compute the sum of their bank accounts. Return the
maximum sum across all customers.

Time Complexity: O(m * n)
Space Complexity: O(1)
*/

class Solution {
    public int maximumWealth(int[][] accounts) {
        int maxWealth = 0;
        for (int[] customer : accounts) {
            int wealth = 0;
            for (int account : customer) {
                wealth += account;
            }
            maxWealth = Math.max(maxWealth, wealth);
        }
        return maxWealth;
    }
}
