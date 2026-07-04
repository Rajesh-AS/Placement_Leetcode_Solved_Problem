"""
LeetCode 1967
Number of Strings That Appear as Substrings in Word

Difficulty: Easy

Approach:
Iterate through each pattern and check if it is a substring of the given
word using Python's 'in' operator. Count the matches and return the total.

Time Complexity: O(n * m * k)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def numOfStrings(self, patterns: List[str], word: str) -> int:
        return sum(1 for pattern in patterns if pattern in word)
