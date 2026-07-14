# LeetCode 3402 - Minimum Operations to Make Columns Strictly Increasing

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/minimum-operations-to-make-columns-strictly-increasing/](https://leetcode.com/problems/minimum-operations-to-make-columns-strictly-increasing/)

## Approach

Process each column independently, top to bottom. If the current element is not strictly greater than the one above it, increase it to `previous + 1`. The number of operations for that cell is `(previous + 1) - current`. Accumulate the total operations across all columns and rows.

## Time Complexity

O(m × n) — every cell is processed once.

## Space Complexity

O(1) — only constant extra variables.
