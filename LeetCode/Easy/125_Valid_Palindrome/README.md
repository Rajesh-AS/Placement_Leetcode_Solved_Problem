# LeetCode 125 - Valid Palindrome

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/valid-palindrome/](https://leetcode.com/problems/valid-palindrome/)

## Approach

Use two pointers — one starting from the beginning and one from the end. Skip non-alphanumeric characters from both sides. Compare the characters case-insensitively. If all matching pairs are equal, the string is a valid palindrome.

## Time Complexity

O(n) — each character is visited at most once.

## Space Complexity

O(1) — only two pointer variables used.
