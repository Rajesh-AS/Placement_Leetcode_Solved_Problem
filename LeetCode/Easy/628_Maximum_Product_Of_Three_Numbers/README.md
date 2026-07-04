# LeetCode 628 - Maximum Product of Three Numbers

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/maximum-product-of-three-numbers/](https://leetcode.com/problems/maximum-product-of-three-numbers/)

## Approach

Sort the array. The maximum product of three numbers is either the product of the three largest numbers, or the product of the two smallest (most negative) numbers and the largest number. Return the maximum of these two candidates.

## Time Complexity

O(n log n) — dominated by sorting.

## Space Complexity

O(1) — sorting in-place; only constant extra space.
