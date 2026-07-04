# LeetCode 1672 - Richest Customer Wealth

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/richest-customer-wealth/](https://leetcode.com/problems/richest-customer-wealth/)

## Approach

For each customer (row in the matrix), compute the sum of all their bank account balances. Track and return the maximum sum across all customers.

## Time Complexity

O(m × n) — where m is the number of customers and n is the number of banks.

## Space Complexity

O(1) — only a max tracker variable.
