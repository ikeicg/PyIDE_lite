import sys


class Lexer:
    def __init__(self, input):
        self.source = input # Feed in source code.
        self.curChar = ''   # Current character in source.
        self.curPos = -1    # Current position in source.
        self.nextChar()

    # Handle the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):     #Check if the current position is out of bounds
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
        while self.curChar == ' '  or self.curChar == '\r':
            self.nextChar()
		
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest.

        if self.curChar == '+':
            token = Token("TT_PLUS", self.curChar)
        elif self.curChar == '-':
            token = Token("TT_MINUS", self.curChar)
        elif self.curChar == '*':
            token = Token("TT_MULT", self.curChar)
        elif self.curChar == '/':
            token = Token("TT_DIV", self.curChar)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token("TT_EQEQ", lastChar + self.curChar)
            else:
                token = Token("TT_EQ", self.curChar)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token("TT_GTEQ", lastChar + self.curChar)
            else:
                token = Token("TT_GT", self.curChar)
        elif self.curChar == '<':
                # Check whether this is token is < or <=
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_LTEQ", lastChar + self.curChar)
                else:
                    token = Token("TT_LT", self.curChar)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token("TT_NTEQ", lastChar + self.curChar)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token("TT_STRING", tokText)
        elif self.curChar == "\'":
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != "\'":
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token("TT_STRING", tokText)
        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit(): 
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token("TT_NUMBER", tokText)
        elif self.curChar.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            keyword = isKeyWord(tokText)
            if not keyword: # Identifier
                token = Token("TT_IDENT", tokText)
            else:   # Keyword
                token = Token("TT_KEYW", tokText)
        elif self.curChar == '(':
            token = Token("TT_LPAREN", self.curChar)
        elif self.curChar == ')':
            token = Token("TT_RPAREN", self.curChar)
        elif self.curChar == '[':
            token = Token("TT_LSQPAREN", self.curChar)
        elif self.curChar == ']':
            token = Token("TT_RSQPAREN", self.curChar)
        elif self.curChar == ':':
            token = Token("TT_COLON", self.curChar)
        elif self.curChar == ',':
            token = Token("TT_COMMA", self.curChar)
        elif self.curChar == '\t':
            token = Token("TT_TAB")
        elif self.curChar == '\n':
            token = Token("TT_NWL")
        elif self.curChar == '\0':
            token = Token("TT_EOF")
        else:
            # Unknown token
            self.abort("Unknown token: " + self.curChar)
			
        self.nextChar()
        return token




def isKeyWord(token):
    keywords = ["if", "while", "print"]
    if token in keywords:
        return True
    return False


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}  :-  {self.value}'
        return f'{self.type}'


# TokenType is our enum for all the types of tokens.
# class TokenType(enum.Enum):
# 	EOF = -1
# 	NEWLINE = 0
# 	NUMBER = 1
# 	IDENT = 2
# 	STRING = 3
# 	# Keywords.
# 	LABEL = 101
# 	GOTO = 102
# 	PRINT = 103
# 	INPUT = 104
# 	LET = 105
# 	IF = 106
# 	THEN = 107
# 	ENDIF = 108
# 	WHILE = 109
# 	REPEAT = 110
# 	ENDWHILE = 111
# 	# Operators.
# 	EQ = 201
# 	PLUS = 202
# 	MINUS = 203
# 	ASTERISK = 204
# 	SLASH = 205
# 	EQEQ = 206
# 	NOTEQ = 207
# 	LT = 208
# 	LTEQ = 209
# 	GT = 210
# 	GTEQ = 211

