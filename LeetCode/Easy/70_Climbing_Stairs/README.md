# LeetCode 70 - Climbing Stairs

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/climbing-stairs/](https://leetcode.com/problems/climbing-stairs/)

## Approach

This is a classic **dynamic programming** problem equivalent to the Fibonacci sequence. The number of ways to reach step `n` equals the sum of ways to reach step `n-1` (taking 1 step) and step `n-2` (taking 2 steps). Use two variables to track the previous two values instead of a full array.

## Time Complexity

O(n) — single loop from 2 to n.

## Space Complexity

O(1) — only two rolling variables.
