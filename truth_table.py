#!/usr/bin/env python3
import sys

class TruthTable(dict):

    def __init__(self, operands):
        self.column_length = (2**len(operands))
        for index, operand in enumerate(operands):
            value = False
            switch_rate = (2**(len(operands)-index)) / 2
            column = []
            for row in range(1, self.column_length+1, 1):
                column.append(value)
                if row % switch_rate == 0:
                    value = not value
            self[operand] = column

    def __str__(self):
        output = ""
        lengths = []
        for column, header in enumerate(list(self.keys())):
            lengths.append(len(header)+2)
            output += '|{:^{length}}'.format(header,  length=lengths[column])
            if column == len(self)-1:
                output += '|\n'
        for i in range(0, len(self), 1):
            output += '+{:-^{length}}'.format('', length=lengths[i])
            if i == len(self)-1:
                output += '+\n'
        for row in range(0, self.column_length, 1):
            for column in range(0, len(self), 1):
                value = 'T' if list(self.values())[column][row] else 'F'
                output += '|{:^{length}}'.format(value, length=lengths[column])
            if column == len(self)-1:
                output += '|\n'            
        return output
        
        
    def negation(self, operands, row):
        operand = self[operands[0]][row]
        return not operand
    
    def conjunction(self, operands, row):
        operand1 = self[operands[0]][row]
        operand2 = self[operands[1]][row]
        return operand1 & operand2

    def disjunction(self, operands, row):
        operand1 = self[operands[0]][row]
        operand2 = self[operands[1]][row]
        return operand1 | operand2

    def implication(self, operands, row):
        operand1 = self[operands[0]][row]
        operand2 = self[operands[1]][row]
        return (not operand1) | operand2
    
    def biconditional(self, operands, row):
        operand1 = self[operands[0]][row]
        operand2 = self[operands[1]][row]
        return not (operand1 ^ operand2)
   
    def evaluate_expression(self, operands, operator):
        if operator == '~':
            expression = operator + operands[0]
        else:
            expression = operands[0] + operator + operands[1]

        if expression in self:
            return

        if   operator == '~':
            function = self.negation
        elif operator == '&':
            function = self.conjunction
        elif operator == '|':
            function = self.disjunction
        elif operator == '>':
            function = self.implication
        elif operator == '=':
            function = self.biconditional
    
        column = []
        for row in range(0, self.column_length, 1):
            column.append(function(operands, row))

        self[expression] = column

    precedence = {
        ')' : 5,
        '~' : 4,
        '&' : 3,
        '|' : 2,
        '>' : 1,
        '=' : 0,
        '(' : -1
    }

    def evaluate_statement(self, statement):
        self.statement = statement

        operator_stack = list()
        operand_stack  = list()

        for char in statement:
            if char ==' ':
                continue
            if char == ')':
                while True:
                    operator = operator_stack.pop()
                    if operator == '(':
                        break
                    operands = []
                    operands.append(operand_stack.pop())
                    if operator == '~':
                        expression = operator + operands[0]
                    else:
                        operands.insert(0, operand_stack.pop())
                        expression = operands[0] + operator + operands[1]
                    self.evaluate_expression(operands, operator)
                    operand_stack.append(expression)
            elif char in self.precedence:        
                while char != '(' and operator_stack and \
                self.precedence[char] < self.precedence[operator_stack[-1]]:
                    operator = operator_stack.pop()
                    operands = []
                    operands.append(operand_stack.pop())
                    if operator == '~':
                        expression = operator + operands[0]
                    else:
                        operands.insert(0, operand_stack.pop())
                        expression = operands[0] + operator + operands[1]
                    self.evaluate_expression(operands, operator)
                    operand_stack.append(expression)
                operator_stack.append(char)
            else :
                operand_stack.append(char)

        while operator_stack:
            operator = operator_stack.pop()
            operands = []
            operands.append(operand_stack.pop())
            if operator == '~':
                expression = operator + operands[0]
            else:
                operands.insert(0, operand_stack.pop())
                expression = operands[0] + operator + operands[1]
            self.evaluate_expression(operands, operator)
            operand_stack.append(expression)

    def simple_statement(self):
        statement_column = list(self.values())[-1]
        minterms = []

        for index, value in enumerate(statement_column):
            if value:
                minterms.append(index)
        
        if not minterms:
            return "Statement is a contradiction."
        elif len(minterms) == len(statement_column):
            return "Statement is a tautology."
        else:
            pass

if __name__ == '__main__':
    if len(sys.argv) == 1 :
        statement = input('Enter a compound propositional statement: ')
    else :
        statement = sys.argv[1]

    print('\nEvaluating {} ...\n'.format(statement))

    operands = set()
    for char in statement :
        if (char not in TruthTable.precedence) and char != ' ':
            operands.add(char)
    operands = sorted(operands)

    table = TruthTable(operands)
    table.evaluate_statement(statement)
    print(table)
    print(table.simple_statement())