# LeetCode 1846 - Maximum Element After Decreasing and Rearranging

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/)

## Approach

Sort the array. Set the first element to 1 (as required). Then iterate left to right — each element can be at most one more than its predecessor. If the current element exceeds `prev + 1`, clamp it down. The final element in the processed array is the answer.

## Time Complexity

O(n log n) — dominated by sorting.

## Space Complexity

O(1) — sorting is in-place; only constant extra variables.
