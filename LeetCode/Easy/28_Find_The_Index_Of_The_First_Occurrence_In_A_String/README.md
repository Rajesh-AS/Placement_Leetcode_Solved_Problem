# LeetCode 28 - Find the Index of the First Occurrence in a String

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)

## Approach

Slide a window of size equal to the needle across the haystack. At each position, compare the substring of length `len(needle)` with the needle. Return the index of the first match. If no match is found, return -1. This is equivalent to using built-in `find()` / `indexOf()`.

## Time Complexity

O(n × m) — where n is the length of haystack and m is the length of needle.

## Space Complexity

O(1) — no extra space beyond a few variables.
