/*
LeetCode 747
Largest Number At Least Twice of Others

Difficulty: Easy

Approach:
Find the maximum and second maximum in a single pass. If the maximum
is at least twice the second maximum, return its index. Otherwise
return -1.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int dominantIndex(int[] nums) {
        int maxIdx = 0;
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > nums[maxIdx]) maxIdx = i;
        }
        for (int i = 0; i < nums.length; i++) {
            if (i != maxIdx && nums[maxIdx] < 2 * nums[i]) return -1;
        }
        return maxIdx;
    }
}
