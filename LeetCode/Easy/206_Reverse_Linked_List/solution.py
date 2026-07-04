"""
LeetCode 206
Reverse Linked List

Difficulty: Easy

Approach:
Iterate through the list using three pointers: prev, curr, and next_node.
At each step, reverse the current node's pointer to point to the previous
node. Advance prev and curr forward until the entire list is reversed.
Return prev as the new head.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev
