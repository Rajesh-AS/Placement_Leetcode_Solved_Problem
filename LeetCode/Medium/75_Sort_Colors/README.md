# LeetCode 75 - Sort Colors

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/sort-colors/](https://leetcode.com/problems/sort-colors/)

## Approach

Use the **Dutch National Flag algorithm** with three pointers: `low`, `mid`, and `high`. Partition the array into three regions — 0s on the left, 1s in the middle, and 2s on the right. When `mid` points to 0, swap with `low` and advance both; when it points to 2, swap with `high` and decrement `high`; when it points to 1, just advance `mid`. This achieves a single-pass in-place sort.

## Time Complexity

O(n) — single pass through the array.

## Space Complexity

O(1) — in-place sorting with three pointers.
