# LeetCode 242 - Valid Anagram

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/valid-anagram/](https://leetcode.com/problems/valid-anagram/)

## Approach

Count the frequency of each character in both strings using a fixed-size array of 26 slots. If both frequency arrays are identical, the strings are anagrams. Alternatively, increment counts for the first string and decrement for the second — if all counts are zero at the end, it is a valid anagram.

## Time Complexity

O(n) — single pass through each string.

## Space Complexity

O(1) — fixed-size array of 26 characters.
