"""
LeetCode 226
Invert Binary Tree

Difficulty: Easy

Approach:
Recursively swap the left and right children of every node. For each
node, swap its two subtrees and then recursively invert each subtree.
Base case: if the node is None, return None.

Time Complexity: O(n)
Space Complexity: O(h)
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
