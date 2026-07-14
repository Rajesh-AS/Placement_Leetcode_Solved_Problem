'''
 Remove unbalanced parentheses in a given expression.

    Eg.) Input  : ((abc)((de))
         Output : ((abc)(de))  

         Input  : (((ab)
         Output : (ab) 
'''
def remove_unbalanced_parentheses(s):
    stack = []
    remove = set()

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack:
                stack.pop()
            else:
                remove.add(i)

    # Remaining '(' are unbalanced
    while stack:
        remove.add(stack.pop())

    result = ""
    for i, ch in enumerate(s):
        if i not in remove:
            result += ch

    return result


# Input
s = input()

# Output
print(remove_unbalanced_parentheses(s))