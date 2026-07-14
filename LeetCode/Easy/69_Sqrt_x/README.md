# LeetCode 69 - Sqrt(x)

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/sqrtx/](https://leetcode.com/problems/sqrtx/)

## Approach

Use **binary search** to find the integer square root. Search in the range `[0, x]`. For each `mid`, check if `mid * mid <= x`. Find the largest `mid` satisfying this condition.

## Time Complexity

O(log x) — binary search over the range [0, x].

## Space Complexity

O(1) — only pointer variables.
