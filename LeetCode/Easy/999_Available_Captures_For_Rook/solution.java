/*
LeetCode 999
Available Captures for Rook

Difficulty: Easy

Approach:
Find the rook position. Scan in four cardinal directions. In each
direction, stop at the first piece: if it's a pawn ('p'), count it
as a capture; if it's a bishop ('B'), stop without capturing.

Time Complexity: O(1)
Space Complexity: O(1)
*/

class Solution {
    public int numRookCaptures(char[][] board) {
        int rookRow = 0, rookCol = 0;
        for (int r = 0; r < 8; r++) {
            for (int c = 0; c < 8; c++) {
                if (board[r][c] == 'R') {
                    rookRow = r;
                    rookCol = c;
                }
            }
        }

        int captures = 0;
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        for (int[] d : dirs) {
            int r = rookRow + d[0], c = rookCol + d[1];
            while (r >= 0 && r < 8 && c >= 0 && c < 8) {
                if (board[r][c] == 'B') break;
                if (board[r][c] == 'p') {
                    captures++;
                    break;
                }
                r += d[0];
                c += d[1];
            }
        }
        return captures;
    }
}
