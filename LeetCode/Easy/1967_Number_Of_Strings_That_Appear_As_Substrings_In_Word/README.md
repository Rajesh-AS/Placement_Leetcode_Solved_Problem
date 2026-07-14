# LeetCode 1967 - Number of Strings That Appear as Substrings in Word

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/](https://leetcode.com/problems/number-of-strings-that-appear-as-substrings-in-word/)

## Approach

For each pattern in the array, check if it exists as a substring in the given word using the `in` operator (Python) or `contains()` (Java). Count and return the number of patterns that are substrings.

## Time Complexity

O(n × m × k) — where n is the number of patterns, m is the average pattern length, and k is the length of the word.

## Space Complexity

O(1) — no extra space beyond a counter.
