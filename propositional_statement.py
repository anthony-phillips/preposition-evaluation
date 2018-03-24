#!/usr/bin/env python3
import sys
from helpers import get_operands

def evaluate(operand1, operand2, operator) :
    pass
    

if len(sys.argv) == 1 :
    statement = input('Enter a compound propositional statement: ')
else :
    statement = sys.argv[1]

print('Evaluating "{}" ...'.format(statement))

# Determine the operands
operands = get_operands(statement)

print('Expression contains {} operands: {}'
    .format(len(operand_set), ", ".join(operand_set)))

rows = list()

# Evaluate the expression
operator_stack = list()
operand_stack  = list()

for char in statement :
    if (char == '(') :
        operator_stack.append(char)
    elif (char in ['~', '>', '<', '&', '|']) :
        while char.compare_precedence(operator_stack[-1]) > 0 :
            pass
    else :
        operand_stack.append(char)

while operator_stack :
    operand1 = operand_stack.pop()
    operand2 = operand_stack.pop()
    operator = operator_stack.pop()
    value = evaluate(operand1, operand2, operator)

print('operators:')
for operator in reversed(operator_stack) :
    print(operator)

print('operands:')
for operand in reversed(operand_stack) :
    print(operand)
