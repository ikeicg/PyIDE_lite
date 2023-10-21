from lexer import *
import sys

def main():
    source = sys.argv[1]
    new_lexer = Lexer(source)

    token = new_lexer.getToken()
    while token.type != "TT_EOF":
        print(token)
        token = new_lexer.getToken()

main()