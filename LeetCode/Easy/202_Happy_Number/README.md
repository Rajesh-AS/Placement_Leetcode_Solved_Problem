# LeetCode 202 - Happy Number

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/happy-number/](https://leetcode.com/problems/happy-number/)

## Approach

Repeatedly replace the number with the sum of the squares of its digits. Use **Floyd's cycle detection** (slow and fast pointers) to detect if the process enters a cycle. If the number reaches 1, it is happy. If a cycle is detected (without reaching 1), it is not happy. This avoids using a hash set.

## Time Complexity

O(log n) — the number of digits decreases or cycles quickly.

## Space Complexity

O(1) — Floyd's cycle detection uses no extra space.
