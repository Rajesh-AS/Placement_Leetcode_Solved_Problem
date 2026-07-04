"""Write a program to give the following output for the given input.

Eg 1: Input: a1b10
       Output: abbbbbbbbbb
Eg: 2: Input: b3c6d15
          Output: bbbccccccddddddddddddddd
The number varies from 1 to 99.
"""
s=input("Enter the string: ")
i=0
res=""
while i<len(s):
    ch=s[i]
    i+=1

    num=""
    while i < len(s)and s[i].isdigit():
        num+=s[i]
        i+=1  
    res+=ch*int(num)
print(res)
