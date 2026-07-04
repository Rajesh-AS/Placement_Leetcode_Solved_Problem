/*
LeetCode 28
Find the Index of the First Occurrence in a String

Difficulty: Easy

Approach:
Slide a window of needle's length across the haystack. Compare the
substring at each position with the needle. Return the first matching
index, or -1 if not found.

Time Complexity: O(n * m)
Space Complexity: O(1)
*/

class Solution {
    public int strStr(String haystack, String needle) {
        return haystack.indexOf(needle);
    }
}
