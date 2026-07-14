"""Write a program to print the following output for the given input. You can assume the string is of odd length

Eg 1: Input: 12345
       Output:
1       5
  2   4
    3
  2  4
1      5"""


s = input()
n = len(s)

# Upper half (including middle)
for i in range((n // 2) + 1):
    if i == n // 2:
        print(" " * (2 * i) + s[i])
    else:
        print(" " * (2 * i) + s[i] + " " * (2 * (n - 2 * i - 1) - 1) + s[n - i - 1])

# Lower half
for i in range(n // 2 - 1, -1, -1):
    print(" " * (2 * i) + s[i] + " " * (2 * (n - 2 * i - 1) - 1) + s[n - i - 1])