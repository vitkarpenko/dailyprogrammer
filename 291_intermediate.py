import math
import collections


def solve_rpn(expression):
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '//': lambda x, y: x // y,
        '%': lambda x, y: x % y,
        '^': lambda x, y: x ** y
    }

    stack = collections.deque()

    for token in expression.split():
        if token == '!':
            stack.append(math.factorial(stack.pop()))
        elif token in operations:
            arguments = [stack.pop(), stack.pop()][::-1]
            stack.append(operations[token](*arguments))
        else:
            stack.append(float(token))

    return stack[0]


print(solve_rpn('100 807 3 331 * + 2 2 1 + 2 + * 5 ^ * 23 10 558 * 10 * + + *'))
