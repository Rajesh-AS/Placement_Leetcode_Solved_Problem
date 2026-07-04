/*
LeetCode 3020
Find the Maximum Number of Elements in Subset

Difficulty: Medium

Approach:
Count frequencies with a hash map. For each base x > 1, build the chain
x -> x^2 -> x^4 -> ... requiring freq >= 2 at each step except the center.
Handle x = 1 separately (odd count of 1s). Return the max chain length.

Time Complexity: O(n log log M)
Space Complexity: O(n)
*/

import java.util.HashMap;
import java.util.Map;

class Solution {
    public int maximumLength(int[] nums) {
        Map<Long, Integer> count = new HashMap<>();
        for (int num : nums) {
            count.merge((long) num, 1, Integer::sum);
        }

        int result = 1;

        if (count.containsKey(1L)) {
            int ones = count.get(1L);
            result = (ones % 2 == 1) ? ones : ones - 1;
        }

        for (long base : count.keySet()) {
            if (base == 1) continue;
            int chainLength = 0;
            long current = base;
            while (count.containsKey(current) && count.get(current) >= 2) {
                chainLength += 2;
                current = current * current;
            }
            if (count.containsKey(current)) {
                chainLength += 1;
            } else {
                chainLength -= 1;
            }
            result = Math.max(result, chainLength);
        }

        return result;
    }
}
