# LeetCode 226 - Invert Binary Tree

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/invert-binary-tree/](https://leetcode.com/problems/invert-binary-tree/)

## Approach

Recursively invert the binary tree by swapping the left and right children of every node. For each node, swap its left and right subtrees, then recursively invert each subtree. The base case is when the node is `null`.

## Time Complexity

O(n) — every node is visited exactly once.

## Space Complexity

O(h) — recursion stack depth equals the height of the tree (O(log n) for balanced, O(n) for skewed).
