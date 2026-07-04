# LeetCode 1358 - Number of Substrings Containing All Three Characters

**Difficulty:** Medium

## Problem Link

[https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/)

## Approach

Use a **sliding window** with the last-seen index of each character (`a`, `b`, `c`). For each position `i`, once all three characters have been seen, the number of valid substrings ending at `i` is `1 + min(last[a], last[b], last[c])` — because any starting index from 0 to that minimum produces a valid substring. Accumulate this count.

## Time Complexity

O(n) — single pass through the string.

## Space Complexity

O(1) — only three index variables.
