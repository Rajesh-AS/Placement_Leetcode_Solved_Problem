/*
LeetCode 242
Valid Anagram

Difficulty: Easy

Approach:
Use a frequency array of size 26. Increment counts for characters in s
and decrement for characters in t. If all counts are zero at the end,
the strings are valid anagrams.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) {
            count[s.charAt(i) - 'a']++;
            count[t.charAt(i) - 'a']--;
        }
        for (int c : count) {
            if (c != 0) return false;
        }
        return true;
    }
}
