# LeetCode 2022 - Convert 1D Array Into 2D Array

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/convert-1d-array-into-2d-array/](https://leetcode.com/problems/convert-1d-array-into-2d-array/)

## Approach

First check if `m × n` equals the length of the original array — if not, return an empty array. Then fill the 2D array row by row, slicing `n` elements at a time from the original array.

## Time Complexity

O(m × n) — every element is placed exactly once.

## Space Complexity

O(1) — excluding the output array.
