"""
LeetCode 1672
Richest Customer Wealth

Difficulty: Easy

Approach:
For each customer, compute the sum of their bank accounts. Return the
maximum sum across all customers.

Time Complexity: O(m * n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def maximumWealth(self, accounts: List[List[int]]) -> int:
        return max(sum(customer) for customer in accounts)
