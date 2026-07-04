"""
LeetCode 58
Length of Last Word

Difficulty: Easy

Approach:
Strip trailing spaces, then iterate from the end counting characters
until a space is found. Return the count as the length of the last word.

Time Complexity: O(n)
Space Complexity: O(1)
"""


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        return len(s.rstrip().split(' ')[-1])
