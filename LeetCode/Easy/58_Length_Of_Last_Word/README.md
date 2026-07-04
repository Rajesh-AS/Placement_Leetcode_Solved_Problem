# LeetCode 58 - Length of Last Word

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/length-of-last-word/](https://leetcode.com/problems/length-of-last-word/)

## Approach

Strip trailing spaces from the string, then iterate from the end counting characters until a space is encountered. The count gives the length of the last word. Alternatively, split by spaces and return the length of the last non-empty token.

## Time Complexity

O(n) — single pass from the end of the string.

## Space Complexity

O(1) — only a counter variable is used.
