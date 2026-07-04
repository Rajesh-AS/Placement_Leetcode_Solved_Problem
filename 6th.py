'''	
Using Recursion reverse the string such as


Eg 1: Input: one two three
      Output: three two one
Eg 2: Input: I love india
      Output: india love I 
'''
def reverse_string(word,index):
    if  index <0:
        return
    print(word[index],end=' ')
    reverse_string(word,index-1)

words = list(input("Enter the string: ").split())
reverse_string(words,len(words)-1)