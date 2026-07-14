/*
LeetCode 75
Sort Colors

Difficulty: Medium

Approach:
Dutch National Flag algorithm. Use three pointers: low, mid, high.
Swap 0s to the front and 2s to the back in a single pass, leaving
1s in the middle. This sorts the array in-place.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            if (nums[mid] == 0) {
                int temp = nums[low];
                nums[low] = nums[mid];
                nums[mid] = temp;
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                int temp = nums[mid];
                nums[mid] = nums[high];
                nums[high] = temp;
                high--;
            }
        }
    }
}
