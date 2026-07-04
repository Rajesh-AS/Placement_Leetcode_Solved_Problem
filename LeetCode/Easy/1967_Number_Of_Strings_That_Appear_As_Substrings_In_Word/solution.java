/*
LeetCode 1967
Number of Strings That Appear as Substrings in Word

Difficulty: Easy

Approach:
Iterate through each pattern and check if it is a substring of the given
word using Java's contains() method. Count the matches and return the total.

Time Complexity: O(n * m * k)
Space Complexity: O(1)
*/

class Solution {
    public int numOfStrings(String[] patterns, String word) {
        int count = 0;
        for (String pattern : patterns) {
            if (word.contains(pattern)) {
                count++;
            }
        }
        return count;
    }
}
