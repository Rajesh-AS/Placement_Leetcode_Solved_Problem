# LeetCode 238 - Product of Array Except Self

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/product-of-array-except-self/](https://leetcode.com/problems/product-of-array-except-self/)

## Approach

Use a two-pass approach without division. In the first pass (left to right), build a prefix product array where each element stores the product of all elements to its left. In the second pass (right to left), multiply each element by the running suffix product (product of all elements to its right). The result array is built in-place during these two passes.

## Time Complexity

O(n) — two linear passes through the array.

## Space Complexity

O(1) — the output array is not counted as extra space per the problem statement.
