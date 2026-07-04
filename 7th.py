'''
Alternate sorting: Given an array of integers, rearrange the array in such a way that the first 
element is first maximum and second element is first minimum.


    Eg.) Input  : {1, 2, 3, 4, 5, 6, 7}
         Output : {7, 1, 6, 2, 5, 3, 4} 
'''
l1=list(map(int,input("elements Array1:").split(',')))
l2=[]
while (len(l1)>0):
    l2.append(max(l1))
    l1.remove(max(l1))
    if len(l1)>0:
        l2.append(min(l1))
        l1.remove(min(l1))
print("Output:", l2)