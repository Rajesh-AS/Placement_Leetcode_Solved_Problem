"""
LeetCode 242
Valid Anagram

Difficulty: Easy

Approach:
Use a frequency array of size 26. Increment counts for characters in s
and decrement for characters in t. If all counts are zero at the end,
the strings are valid anagrams.

Time Complexity: O(n)
Space Complexity: O(1)
"""


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        count = [0] * 26
        for i in range(len(s)):
            count[ord(s[i]) - ord('a')] += 1
            count[ord(t[i]) - ord('a')] -= 1
        return all(c == 0 for c in count)
