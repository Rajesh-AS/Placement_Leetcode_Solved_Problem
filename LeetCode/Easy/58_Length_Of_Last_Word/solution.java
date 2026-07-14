/*
LeetCode 58
Length of Last Word

Difficulty: Easy

Approach:
Strip trailing spaces, then iterate from the end counting characters
until a space is found. Return the count as the length of the last word.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int lengthOfLastWord(String s) {
        s = s.trim();
        int length = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            if (s.charAt(i) == ' ') break;
            length++;
        }
        return length;
    }
}
