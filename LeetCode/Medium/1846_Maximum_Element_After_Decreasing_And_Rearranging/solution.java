/*
LeetCode 1846
Maximum Element After Decreasing and Rearranging

Difficulty: Medium

Approach:
Sort the array. Set the first element to 1. Iterate through the array
ensuring each element is at most prev + 1. The last element after
processing gives the maximum possible value.

Time Complexity: O(n log n)
Space Complexity: O(1)
*/

import java.util.Arrays;

class Solution {
    public int maximumElementAfterDecrementingAndRearranging(int[] arr) {
        Arrays.sort(arr);
        int prev = 0;
        for (int num : arr) {
            prev = Math.min(num, prev + 1);
        }
        return prev;
    }
}
