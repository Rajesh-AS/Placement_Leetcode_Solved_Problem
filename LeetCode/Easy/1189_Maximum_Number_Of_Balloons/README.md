# LeetCode 1189 - Maximum Number of Balloons

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/maximum-number-of-balloons/](https://leetcode.com/problems/maximum-number-of-balloons/)

## Approach

Count the frequency of each character in the given string. The word **"balloon"** requires specific character counts: `b(1)`, `a(1)`, `l(2)`, `o(2)`, `n(1)`. For each character needed, compute how many times it can contribute to forming the word — dividing by 2 for `l` and `o` since they appear twice. The answer is the minimum across all five required characters.

## Time Complexity

O(n) — single pass through the string to count character frequencies.

## Space Complexity

O(1) — only a fixed-size counter (at most 26 characters) is used.
