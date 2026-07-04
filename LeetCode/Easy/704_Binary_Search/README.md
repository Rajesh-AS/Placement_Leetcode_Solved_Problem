# LeetCode 704 - Binary Search

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/binary-search/](https://leetcode.com/problems/binary-search/)

## Approach

Classic binary search on a sorted array. Maintain two pointers `left` and `right`. Compute `mid` and compare `nums[mid]` with the target. If equal, return `mid`. If target is smaller, search the left half; otherwise search the right half. Return -1 if the target is not found.

## Time Complexity

O(log n) — the search space is halved in every iteration.

## Space Complexity

O(1) — only constant extra space is used.
