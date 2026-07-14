/*
LeetCode 238
Product of Array Except Self

Difficulty: Medium

Approach:
Two-pass approach without division. First pass builds prefix products
from left to right. Second pass multiplies a running suffix product
from right to left. Each position ends up with the product of all
elements except itself.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        result[0] = 1;
        for (int i = 1; i < n; i++) {
            result[i] = result[i - 1] * nums[i - 1];
        }
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] *= suffix;
            suffix *= nums[i];
        }
        return result;
    }
}
