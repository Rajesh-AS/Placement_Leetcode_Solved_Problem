"""
LeetCode 1189
Maximum Number of Balloons

Difficulty: Easy

Approach:
Count character frequencies in the input string. The word "balloon"
needs b(1), a(1), l(2), o(2), n(1). For each required character,
determine how many complete contributions it can make (dividing by 2
for 'l' and 'o'). Return the minimum across all five characters.

Time Complexity: O(n)
Space Complexity: O(1)
"""

from collections import Counter


class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        count = Counter(text)
        return min(
            count['b'],
            count['a'],
            count['l'] // 2,
            count['o'] // 2,
            count['n']
        )
