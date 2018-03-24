#!/usr/bin/env python3
import sys
from truth_table import TruthTable
    
# Get statement
if len(sys.argv) == 1 :
    statement = input('Enter a compound propositional statement: ')
else :
    statement = sys.argv[1]

print('\nEvaluating {} ...\n'.format(statement))

operands = set()
for char in statement :
    if (char not in ['(', ')', '~', '>', '&', '|']) :
        operands.add(char)
operands = sorted(operands)

table = TruthTable(operands)
table.evaluate_statement(statement)
print(table)
print(table.simple_statement())