#!/usr/bin/env python3
import sys

if len(sys.argv) == 1 :
    statement = input('Enter a compound propositional statement: ')
else :
    statement = sys.argv[1]

print('Evaluating "{}" ...'.format(statement))

operandSet = set()

for char in statement :
    if (char not in ['(', ')', '~', '>', '<', '&', '|']) :
        operandSet.add(char)

operandSet = sorted(operandSet)

print('Expression contains {} operators: {}'
      .format(len(operandSet), ", ".join(operandSet)))

operatorStack = []
operandStack = []

for char in statement :
    if (char in ['(', ')', '~', '>', '<', '&', '|']) :
        operatorStack.append(char)
    else :
        operandStack.append(char)

print('operators:')
for operator in reversed(operatorStack) :
    print(operator)

print('operands:')
for operand in reversed(operandStack) :
    print(operand)