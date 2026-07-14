# LeetCode 3020 - Find the Maximum Number of Elements in Subset

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/](https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/)

## Approach

Count the frequency of each number using a hash map. For each unique number `x` (where `x > 1`), try to build the longest chain `x, x², x⁴, x⁸, ...` where each power exists in the array with frequency ≥ 2 (since the pattern is symmetric: `x, x², ..., x^k, ..., x², x`). The center element needs only frequency ≥ 1. Handle `x = 1` as a special case — take as many 1s as possible (must be an odd count for symmetry). Track the maximum chain length.

## Time Complexity

O(n log log M) — where M is the maximum value; each chain is bounded by log log M powers.

## Space Complexity

O(n) — for the frequency hash map.
