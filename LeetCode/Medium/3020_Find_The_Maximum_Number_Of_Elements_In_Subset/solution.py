"""
LeetCode 3020
Find the Maximum Number of Elements in Subset

Difficulty: Medium

Approach:
Count frequencies with a hash map. For each base x > 1, build the chain
x -> x^2 -> x^4 -> ... requiring freq >= 2 at each step except the center.
Handle x = 1 separately (odd count of 1s). Return the max chain length.

Time Complexity: O(n log log M)
Space Complexity: O(n)
"""

from typing import List
from collections import Counter


class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        count = Counter(nums)
        result = 1

        if 1 in count:
            ones = count[1]
            result = ones if ones % 2 == 1 else ones - 1

        for base in count:
            if base == 1:
                continue
            chain_length = 0
            current = base
            while current in count and count[current] >= 2:
                chain_length += 2
                current = current * current
            if current in count:
                chain_length += 1
            else:
                chain_length -= 1
            result = max(result, chain_length)

        return result
