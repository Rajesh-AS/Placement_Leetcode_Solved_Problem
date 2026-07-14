# LeetCode 206 - Reverse Linked List

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/reverse-linked-list/](https://leetcode.com/problems/reverse-linked-list/)

## Approach

Use three pointers — `prev`, `curr`, and `next_node` — to reverse the linked list iteratively. At each step, save the next node, point the current node's `next` to the previous node, then advance both `prev` and `curr` forward. After the loop, `prev` points to the new head of the reversed list. This is one of the most frequently asked interview questions.

## Time Complexity

O(n) — each node is visited exactly once.

## Space Complexity

O(1) — only a constant number of pointers are used.
