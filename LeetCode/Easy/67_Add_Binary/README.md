# LeetCode 67 - Add Binary

**Difficulty:** Easy

## Problem Link

[https://leetcode.com/problems/add-binary/](https://leetcode.com/problems/add-binary/)

## Approach

Iterate from the rightmost digits of both binary strings, adding corresponding digits along with a carry. At each step, compute the sum (digit from `a` + digit from `b` + carry), append `sum % 2` to the result, and update the carry to `sum // 2`. After processing all digits, if a carry remains, append it. Reverse the result string.

## Time Complexity

O(max(m, n)) — where m and n are the lengths of the two strings.

## Space Complexity

O(max(m, n)) — for the result string.
