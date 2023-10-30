from lexer import *
from parser import *
from interpreter import *
import sys

def main():
    source = sys.argv[1]
    new_lexer = Lexer(source)

    tokens = new_lexer.getTokens()

    # for i in tokens:
    #     print(i)

    new_parser = Parser(tokens)
    asts = new_parser.runParse()

    # print(asts)

    new_interpreter = Interpreter(asts)
    new_interpreter.execute()

main()