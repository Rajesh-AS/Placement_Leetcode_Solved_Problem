/*
LeetCode 1189
Maximum Number of Balloons

Difficulty: Easy

Approach:
Count character frequencies in the input string. The word "balloon"
needs b(1), a(1), l(2), o(2), n(1). For each required character,
determine how many complete contributions it can make (dividing by 2
for 'l' and 'o'). Return the minimum across all five characters.

Time Complexity: O(n)
Space Complexity: O(1)
*/

class Solution {
    public int maxNumberOfBalloons(String text) {
        int[] count = new int[26];
        for (char c : text.toCharArray()) {
            count[c - 'a']++;
        }
        int result = count['b' - 'a'];
        result = Math.min(result, count['a' - 'a']);
        result = Math.min(result, count['l' - 'a'] / 2);
        result = Math.min(result, count['o' - 'a'] / 2);
        result = Math.min(result, count['n' - 'a']);
        return result;
    }
}
