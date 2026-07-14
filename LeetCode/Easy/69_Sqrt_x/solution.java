/*
LeetCode 69
Sqrt(x)

Difficulty: Easy

Approach:
Binary search in range [0, x]. Find the largest mid where mid * mid <= x.
This gives the integer (floor) square root.

Time Complexity: O(log x)
Space Complexity: O(1)
*/

class Solution {
    public int mySqrt(int x) {
        long left = 0, right = x;
        int result = 0;
        while (left <= right) {
            long mid = left + (right - left) / 2;
            if (mid * mid <= x) {
                result = (int) mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return result;
    }
}
