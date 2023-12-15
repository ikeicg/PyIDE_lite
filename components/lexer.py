from PyIDE_lite.components.classfile import *

class Lexer:

    def __init__(self, input, inputPos):
        self.source = input # Feed in source code.
        self.sourcePos = inputPos
        self.curChar = ''   # Current character in source.
        self.curPos = -1    # Current position in source.
        self.tokenList = []
        self.nextChar()

    # Handle the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):     # Check if the current position is out of bounds
            self.curChar = '\0'  # End Of File
        else:
            self.curChar = self.source[self.curPos]

    # Seek / Return the next character .
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar in " \r\t":
            self.nextChar()
		
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            while self.curPos <= len(self.source):
                self.nextChar()

    # Return the next token.
    def tokenize(self):

        while self.curPos < len(self.source):

            self.skipWhitespace()
            self.skipComment()
            token = None

            if self.curChar == '+':
                token = Token("TT_PLUS", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '-':
                token = Token("TT_MINUS", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '*':
                if self.peek() == '*':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_POW", lastChar + self.curChar, self.curPos - 1, self.curPos)
                else:
                    token = Token("TT_MULT", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '/':
                token = Token("TT_DIV", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '=':
                # Check whether this token is = or ==
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_EQEQ", lastChar + self.curChar, self.curPos-1, self.curPos)
                else:
                    token = Token("TT_EQ", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '>':
                # Check whether this is token is > or >=
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_GTEQ", lastChar + self.curChar, self.curPos-1, self.curPos)
                else:
                    token = Token("TT_GT", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '<':
                    # Check whether this is token is < or <=
                    if self.peek() == '=':
                        lastChar = self.curChar
                        self.nextChar()
                        token = Token("TT_LTEQ", lastChar + self.curChar, self.curPos-1, self.curPos)
                    else:
                        token = Token("TT_LT", self.curChar, self.curPos, self.curPos)
                    self.tokenList.append(token)
            elif self.curChar == '!':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_NTEQ", lastChar + self.curChar, self.curPos, self.curPos)
                else:
                    message = "Expected !=, got !" + self.peek()
                    return ['None',
                            Error("Lexing Error", self.source, self.sourcePos, self.curPos, message)
                            ]
                    # self.abort("Expected !=, got !" + self.peek())
                self.tokenList.append(token)
            elif self.curChar == '\"':
                # Get characters between quotations.
                self.nextChar()
                startPos = self.curPos

                while self.curChar != '\"':
                    # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                    if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                        message = "Illegal character in string."
                        return ['None',
                                Error("Lexing Error", self.source, self.sourcePos, self.curPos, message)
                                ]
                        # self.abort("Illegal character in string.")
                    self.nextChar()

                tokText = self.source[startPos : self.curPos+1] # Get the substring.
                token = Token("TT_STRING", tokText, startPos-1, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == "\'":
                # Get characters between quotations.
                self.nextChar()
                startPos = self.curPos

                while self.curChar != "\'":
                    # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                    if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                        message = "Illegal character in string."
                        return ['None',
                                Error("Lexing Error", self.source, self.sourcePos, self.curPos, message)
                                ]
                        # self.abort("Illegal character in string.")
                    self.nextChar()

                tokText = self.source[startPos : self.curPos+1] # Get the substring.
                token = Token("TT_STRING", tokText, startPos-1, self.curPos)
                self.tokenList.append(token)
            elif self.curChar.isdigit():
                # Leading character is a digit, so this must be a number.
                # Get all consecutive digits and decimal if there is one.
                startPos = self.curPos
                while self.peek().isdigit():
                    self.nextChar()

                if self.peek().isalpha():
                    message = f"Invalid Identifier beginning with: {self.source[startPos: self.curPos + 1]}"
                    return ['None',
                            Error("Lexing Error", self.source, self.sourcePos, self.curPos, message)
                            ]

                elif self.peek() == '.': # Decimal!
                    self.nextChar()

                    # Must have at least one digit after decimal.
                    if not self.peek().isdigit():
                        message = "Illegal character in number."
                        return ['None',
                                Error("Lexing Error", self.source, self.sourcePos, self.curPos, message)
                                ]
                        # self.abort("Illegal character in number.")
                    while self.peek().isdigit():
                        self.nextChar()

                tokText = self.source[startPos : self.curPos + 1] # Get the substring.
                token = Token("TT_NUMBER", tokText, startPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar.isalpha():
                # Leading character is a letter, so this must be an identifier or a keyword.
                # Get all consecutive alpha_numeric characters.

                startPos = self.curPos
                while (self.peek().isalnum() or self.peek() == '_'):
                    self.nextChar()

                # Check if the token is in the list of keywords.
                tokText = self.source[startPos : self.curPos + 1] # Get the substring.
                keyword = self.isKeyWord(tokText)
                if not keyword: # Identifier
                    token = IdentToken("TT_IDENT", tokText, startPos, self.curPos)
                else:   # Keyword
                    token = Token("TT_KEYW", tokText, startPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '(':
                token = Token("TT_LPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ')':
                token = Token("TT_RPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '[':
                token = Token("TT_LSQPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ']':
                token = Token("TT_RSQPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ':':
                token = Token("TT_COLON", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ',':
                token = Token("TT_COMMA", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '\t':
                token = Token("TT_TAB", '',  self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '\n':
                token = Token("TT_NWL", '', self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '\0':
                break
            else:
                # Unknown token
                message = "Unknown lexeme: " + self.curChar
                return ['None',
                        Error("Lexing Error", self.source, self.sourcePos, self.curPos, message)
                        ]

            self.nextChar()

        self.tokenList.append(Token("TT_EOF", "", len(self.source), len(self.source)))
        return [self.tokenList, None]

    def isKeyWord(self, token):
        keywords = ["print", "memory"]
        if token in keywords:
            return True
        return False