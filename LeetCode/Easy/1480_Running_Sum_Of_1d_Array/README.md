# LeetCode 1480 - Running Sum of 1d Array

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/running-sum-of-1d-array/](https://leetcode.com/problems/running-sum-of-1d-array/)

## Approach

Iterate through the array starting from index 1. At each position, add the previous element's running sum to the current element. This modifies the array in-place to hold cumulative sums.

## Time Complexity

O(n) — single pass through the array.

## Space Complexity

O(1) — in-place modification, no extra space.
