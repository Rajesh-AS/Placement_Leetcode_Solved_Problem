# LeetCode 1486 - XOR Operation in an Array

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/xor-operation-in-an-array/](https://leetcode.com/problems/xor-operation-in-an-array/)

## Approach

The array is defined as `nums[i] = start + 2 * i`. Simply XOR all elements from index 0 to n-1. Initialize a result variable to 0 and XOR each computed element into it.

## Time Complexity

O(n) — single loop through all n elements.

## Space Complexity

O(1) — only a single result variable.
