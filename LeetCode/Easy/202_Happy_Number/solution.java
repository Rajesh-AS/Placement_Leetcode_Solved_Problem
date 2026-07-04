/*
LeetCode 202
Happy Number

Difficulty: Easy

Approach:
Use Floyd's cycle detection. Compute the sum of squares of digits
repeatedly with a slow and fast pointer. If fast reaches 1, the
number is happy. If slow meets fast, a cycle exists and it's not happy.

Time Complexity: O(log n)
Space Complexity: O(1)
*/

class Solution {
    private int getNext(int n) {
        int total = 0;
        while (n > 0) {
            int digit = n % 10;
            total += digit * digit;
            n /= 10;
        }
        return total;
    }

    public boolean isHappy(int n) {
        int slow = n;
        int fast = getNext(n);
        while (fast != 1 && slow != fast) {
            slow = getNext(slow);
            fast = getNext(getNext(fast));
        }
        return fast == 1;
    }
}
