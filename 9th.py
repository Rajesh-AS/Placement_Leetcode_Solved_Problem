'''
4) Check whether a given mathematical expression is valid.

    Eg.) Input  : (a+b)(a*b)
         Output : Valid

         Input  : (ab)(ab+)
         Output : Invalid

         Input  : ((a+b)
         Output : Invalid 
'''
def is_valid_expression(expr):
    stack = []
    operators = "+-*/"

    # Check balanced parentheses
    for ch in expr:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            if not stack:
                return "Invalid"
            stack.pop()

    if stack:
        return "Invalid"

    # Check operator placement
    n = len(expr)

    for i in range(n):
        if expr[i] in operators:
            # Operator at beginning or end
            if i == 0 or i == n - 1:
                return "Invalid"

            # Consecutive operators
            if expr[i - 1] in operators or expr[i + 1] in operators:
                return "Invalid"

            # Operator after '('
            if expr[i - 1] == '(':
                return "Invalid"

            # Operator before ')'
            if expr[i + 1] == ')':
                return "Invalid"

    return "Valid"


# Input
expression = input()

# Output
print(is_valid_expression(expression))
