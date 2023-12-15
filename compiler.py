from components.lexer import *
from components.parser import *
import sys

source = sys.argv[1]

source = [[i, x] for i, x in enumerate(source.split("\n")) if x != ""]

class Compiler:

    def __init__(self, sourcecode):
        self.sourcecode = sourcecode

    def main(self):

        IR = []   # Use this to batch process the entire source code to Intermediate Representation

        if(len(source) > 0):
            for line in source:

                i, x = line
                new_lexer = Lexer(x, i + 1)

                tokens, error = new_lexer.tokenize()

                if (error):
                    print(error)
                    return -1

                new_parser = Parser(x, tokens, i + 1)

                AST, error2 = new_parser.parseTokens()

                if (error2):
                    print(error2[0])
                    return -1

                if(AST):
                    IR.append(AST)


        # Optimize the Intermediate Representation

        Opt_IR = self.optimizer(IR)


        with open('bytecode.txt', 'w') as file:
            for ast in Opt_IR:
                byte_code = ast.gen_bytecode()
                for opcode in byte_code:
                    file.write(f"{opcode}\n")

        VirtualMachine().run()


    def optimizer(self, IR):
        unique_identifiers = {x.identifier for x in IR if isinstance(x, AssignStmt)}
        identifiers = [[identifier, False] for identifier in unique_identifiers]

        for ast in IR:
            ids = ast.dfa()
            for i in identifiers:
                if i[0] in ids:
                    i[1] = True

        identifiers = [x[0] for x in identifiers if (x[1] == True)]

        IR = [x for x in IR if ((not isinstance(x, AssignStmt)) or (isinstance(x, AssignStmt) and (x.identifier in (identifiers))))]
        return IR


class VirtualMachine:
    def __init__(self):
        self.bytecode = ''
        self.datastore = {}
        self.datastack = []

    def run(self):
        with open("bytecode.txt", "r") as file:
            self.bytecode = file.read()

        self.bytecode = [line.split(':') for line in self.bytecode.split("\n") if line.strip()]

        for opcode, operand in self.bytecode:
            # print(opcode, operand)
            if opcode == 'STORE_NAME':
                self.datastore[operand] = self.datastack.pop()
            elif opcode == 'LOAD_NAME':
                try:
                    self.datastack.append(self.datastore[operand])
                except:
                    sys.exit(f"Runtime Error: Cannot read variable '{operand}'")
            elif opcode == 'LOAD_CONST':
                if operand == "memory":
                    self.datastack.append(self.datastore)
                if operand.isdigit():
                    self.datastack.append(float(operand))
            elif opcode.startswith('BINARY_'):
                b = float(self.datastack.pop())
                a = float(self.datastack.pop())

                if opcode == 'BINARY_ADD':
                    self.datastack.append(a + b)
                elif opcode == 'BINARY_SUBTRACT':
                    self.datastack.append(a - b)
                elif opcode == 'BINARY_MULT':
                    self.datastack.append(a * b)
                elif opcode == 'BINARY_DIV':
                    if b == 0:
                        sys.exit("Runtime Error: Division by zero")
                    else:
                        self.datastack.append(a / b)
                elif opcode == 'BINARY_PLUS':
                    self.datastack.append(a + b)
                elif opcode == 'BINARY_MINUS':
                    self.datastack.append(a - b)
                elif opcode == 'BINARY_POW':
                    self.datastack.append(a ** b)
            elif opcode == 'PRINT':
                value = self.datastack.pop()
                if type(value) in [int, float]:
                    print(round(value, 2))
                else:
                    print(value)
            else:
                sys.exit(f"Runtime Error: Unknown opcode '{opcode}'")


Compiler(source).main()