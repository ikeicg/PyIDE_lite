from components.lexer import *
from components.parser import *
import sys

source = sys.argv[1]

source = [[i, x] for i, x in enumerate(source.split("\n")) if x != ""]

class Interpreter:

    def __init__(self, sourcecode):
        self.sourcecode = sourcecode
        self.datastack = {}

    def main(self):

        if(len(source) > 0):

            # Interpret Source Code Line by Line

            for line in source:

                # Lexing

                i, x = line
                new_lexer = Lexer(x, i + 1)

                tokens, error = new_lexer.tokenize()

                # Handle Lexing Errors

                if (error):
                    print(error)
                    return -1

                # Parsing

                new_parser = Parser(x, tokens, i + 1)

                AST, error2 = new_parser.parseTokens()

                # Handle Parsing Errors

                if (error2):
                    print(error2[0])
                    return -1

                # Execute AST

                if(AST):
                    self.execute(AST)


    def execute(self, ast):

        if(isinstance(ast, PrintStmt)):
            if(ast.value.type == 'memory'):
                print(f"Computer Memory:: {self.datastack}")
                return 0
            if type(ast.value.read(self)) in [int, float]:
                print(round(ast.value.read(self), 2))
            else:
                print(ast.value.read(self))

        elif(isinstance(ast, AssignStmt)):
            self.datastack[ast.identifier] = ast.value.read(self)


Interpreter(source).main()