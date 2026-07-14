"""
Given two sorted arrays

, merge them such that the elements are not repeated

Eg 1: Input:
        Array 1: 2,4,5,6,7,9,10,13
        Array 2: 2,3,4,5,6,7,8,9,11,15
       Output:
       Merged array: 2,3,4,5,6,7,8,9,10,11,13,15 
"""
a1=list(map(int,input("Enter Array 1: ").split(",")))
a2=list(map(int,input("Enter Array 2: ").split(",")))   
res=set(a1+a2)
print ("Merged array: ",end="")
print (*sorted(res),sep=",")