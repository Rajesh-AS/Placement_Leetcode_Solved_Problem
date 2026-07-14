/*
LeetCode 67
Add Binary

Difficulty: Easy

Approach:
Iterate from the rightmost digits of both strings. Add corresponding
digits with carry. Append sum % 2 to result, update carry to sum / 2.
Reverse the result string at the end.

Time Complexity: O(max(m, n))
Space Complexity: O(max(m, n))
*/

class Solution {
    public String addBinary(String a, String b) {
        StringBuilder result = new StringBuilder();
        int carry = 0;
        int i = a.length() - 1, j = b.length() - 1;
        while (i >= 0 || j >= 0 || carry > 0) {
            int total = carry;
            if (i >= 0) total += a.charAt(i--) - '0';
            if (j >= 0) total += b.charAt(j--) - '0';
            result.append(total % 2);
            carry = total / 2;
        }
        return result.reverse().toString();
    }
}
