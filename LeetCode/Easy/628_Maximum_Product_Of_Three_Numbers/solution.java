/*
LeetCode 628
Maximum Product of Three Numbers

Difficulty: Easy

Approach:
Sort the array. The max product is either the product of the three largest
numbers or the product of the two smallest (negative) numbers and the
largest number. Return the maximum of both candidates.

Time Complexity: O(n log n)
Space Complexity: O(1)
*/

import java.util.Arrays;

class Solution {
    public int maximumProduct(int[] nums) {
        Arrays.sort(nums);
        int n = nums.length;
        return Math.max(
            nums[n - 1] * nums[n - 2] * nums[n - 3],
            nums[0] * nums[1] * nums[n - 1]
        );
    }
}
