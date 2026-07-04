 
"""
Find if a String2 is substring of String1

. If it is, return the index of the first occurrence. else return -1.

Eg 1:Input:
        String 1: test123string
         String 2: 123
        Output: 4
Eg 2: Input:
        String 1: testing12
        String 2: 1234 
        Output: -1
"""
s1=input("Enter String 1: ")
s2=input("Enter String 2: ")
if s2 in s1:
    print(s1.index(s2))
else:
    print(-1)
