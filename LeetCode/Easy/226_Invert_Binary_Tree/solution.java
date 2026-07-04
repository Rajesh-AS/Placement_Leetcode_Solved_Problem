/*
LeetCode 226
Invert Binary Tree

Difficulty: Easy

Approach:
Recursively swap the left and right children of every node. For each
node, swap its two subtrees and then recursively invert each subtree.
Base case: if the node is null, return null.

Time Complexity: O(n)
Space Complexity: O(h)
*/

class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        TreeNode temp = root.left;
        root.left = root.right;
        root.right = temp;
        invertTree(root.left);
        invertTree(root.right);
        return root;
    }
}
