"""
LeetCode 1358
Number of Substrings Containing All Three Characters

Difficulty: Medium

Approach:
Track the last seen index of 'a', 'b', and 'c'. For each position i,
the number of valid substrings ending at i is 1 + min(last[a], last[b],
last[c]). Accumulate this count across all positions.

Time Complexity: O(n)
Space Complexity: O(1)
"""


class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        last = [-1, -1, -1]
        result = 0
        for i, char in enumerate(s):
            last[ord(char) - ord('a')] = i
            result += 1 + min(last)
        return result
