/*
LeetCode 1358
Number of Substrings Containing All Three Characters

Difficulty: Medium

Approach:
Track the last seen index of 'a', 'b', and 'c'. For each position i,
the number of valid substrings ending at i is 1 + min(last[a], last[b],
last[c]). Accumulate this count across all positions.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int numberOfSubstrings(String s) {
        int[] last = {-1, -1, -1};
        int result = 0;
        for (int i = 0; i < s.length(); i++) {
            last[s.charAt(i) - 'a'] = i;
            result += 1 + Math.min(last[0], Math.min(last[1], last[2]));
        }
        return result;
    }
}
