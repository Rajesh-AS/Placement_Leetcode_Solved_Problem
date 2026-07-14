 
"""
Write a program to sort the elements in odd positions in descending order and elements in ascending order

Eg 1: Input: 13,2 4,15,12,10,5
        Output: 13,2,12,10,5,15,4
Eg 2: Input: 1,2,3,4,5,6,7,8,9
        Output: 9,2,7,4,5,6,3,8,1 

"""
arr = list(map(int, input().split(",")))

odd = []
even = []

# Separate odd and even positions (1-based)
for i in range(len(arr)):
    if i % 2 == 0:
        odd.append(arr[i])      # 1st, 3rd, 5th...
    else:
        even.append(arr[i])     # 2nd, 4th, 6th...

# Sort
odd.sort(reverse=True)
even.sort()

odd_index = 0
even_index = 0

# Place back into original positions
for i in range(len(arr)):
    if i % 2 == 0:
        arr[i] = odd[odd_index]
        odd_index += 1
    else:
        arr[i] = even[even_index]
        even_index += 1

print(*arr, sep=",")