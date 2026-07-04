'''
Find the minimum number of times required to represent a number as sum of squares.

12 = 1^2 + 1^2 + 1^2 + 1^2 + 1^2 + 1^2 + 
    1^2 + 1^2 + 1^2 + 1^2 + 1^2 + 1^2 
12 = 2^2 + 2^2 + 2^2
12 = 3^2 + 1^2 + 1^2

Input: 12
Output: min: 3
'''
def min_squares(n):
    dp = [0] + [float('inf')] * n

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]


# Input
n = int(input())

# Output
print("min:", min_squares(n))