/*
LeetCode 206
Reverse Linked List

Difficulty: Easy

Approach:
Iterate through the list using three pointers: prev, curr, and nextNode.
At each step, reverse the current node's pointer to point to the previous
node. Advance prev and curr forward until the entire list is reversed.
Return prev as the new head.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nextNode = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextNode;
        }
        return prev;
    }
}
