# LeetCode 3417 - Zigzag Grid Traversal With Skip

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/zigzag-grid-traversal-with-skip/](https://leetcode.com/problems/zigzag-grid-traversal-with-skip/)

## Approach

Traverse the grid in zigzag order: even-indexed rows go left to right, odd-indexed rows go right to left. Flatten this zigzag traversal into a single sequence, then pick every other element (skip alternately). Collect the non-skipped elements into the result.

## Time Complexity

O(m × n) — every cell is visited once.

## Space Complexity

O(1) — excluding the output array.
