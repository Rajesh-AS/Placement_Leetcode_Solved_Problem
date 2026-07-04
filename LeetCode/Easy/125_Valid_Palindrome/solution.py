"""
LeetCode 125
Valid Palindrome

Difficulty: Easy

Approach:
Two pointers from both ends. Skip non-alphanumeric characters. Compare
characters case-insensitively. If all matching pairs are equal, it is
a valid palindrome.

Time Complexity: O(n)
Space Complexity: O(1)
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
