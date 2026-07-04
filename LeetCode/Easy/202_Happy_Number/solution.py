"""
LeetCode 202
Happy Number

Difficulty: Easy

Approach:
Use Floyd's cycle detection. Compute the sum of squares of digits
repeatedly with a slow and fast pointer. If fast reaches 1, the
number is happy. If slow meets fast, a cycle exists and it's not happy.

Time Complexity: O(log n)
Space Complexity: O(1)
"""


class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(number):
            total = 0
            while number > 0:
                digit = number % 10
                total += digit * digit
                number //= 10
            return total

        slow = n
        fast = get_next(n)
        while fast != 1 and slow != fast:
            slow = get_next(slow)
            fast = get_next(get_next(fast))
        return fast == 1
