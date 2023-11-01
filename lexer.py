import sys


class Lexer:
    def __init__(self, input):
        self.source = input # Feed in source code.
        self.curChar = ''   # Current character in source.
        self.curPos = -1    # Current position in source.
        self.tokenList = []
        self.error = None
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
    def getTokens(self):

        while self.curChar != '\0':

            self.skipWhitespace()
            self.skipComment()
            token = None

            # Check the first character of this token to see if we can decide what it is.
            # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest.

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
                    self.abort("Expected !=, got !" + self.peek())
                self.tokenList.append(token)
            elif self.curChar == '\"':
                # Get characters between quotations.
                self.nextChar()
                startPos = self.curPos

                while self.curChar != '\"':
                    # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                    if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                        self.abort("Illegal character in string.")
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
                        self.abort("Illegal character in string.")
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
                if self.peek() == '.': # Decimal!
                    self.nextChar()

                    # Must have at least one digit after decimal.
                    if not self.peek().isdigit():
                        # Error!
                        self.abort("Illegal character in number.")
                    while self.peek().isdigit():
                        self.nextChar()

                tokText = self.source[startPos : self.curPos + 1] # Get the substring.
                token = Token("TT_NUMBER", tokText, startPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar.isalpha():
                # Leading character is a letter, so this must be an identifier or a keyword.
                # Get all consecutive alpha numeric characters.
                startPos = self.curPos
                while self.peek().isalnum():
                    self.nextChar()

                if self.source[startPos - 1].isdigit():
                    self.abort(f"Invalid Identifier: {self.source[startPos-1 : self.curPos +1]}")

                # Check if the token is in the list of keywords.
                tokText = self.source[startPos : self.curPos + 1] # Get the substring.
                keyword = isKeyWord(tokText)
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
            # elif self.curChar == '\0':
            #     token = Token("TT_EOF", self.curPos, self.curPos)
            #     self.tokenList.append(token)
            else:
                # Unknown token
                self.abort("Unknown token: " + self.curChar)

            self.nextChar()

        self.tokenList.append(Token("TT_EOF"))
        return self.tokenList



def isKeyWord(token):
    keywords = ["if", "while", "print"]
    if token in keywords:
        return True
    return False


class Token:
    def __init__(self, type_, value=None, start=None, end=None):
        self.type = type_
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        if self.value: return f'{self.type}:\"{self.value}\"'
        return f'{self.type}'

    def read(self, obj):
        if(self.value):
            if self.type == "TT_NUMBER":
                self.value = float(self.value)
            return self.value
        else:
            return None


class IdentToken(Token):
    def __init__(self, type_, value=None, start=None, end=None):
        super().__init__(type_, value, start, end)

    def __repr__(self):
        if self.value:
            return f'{self.type}:\"{self.value}\"'
        return f'{self.type}'

    def read(self, obj):

        try:
            if obj.datastack[self.value]:
                return obj.datastack[self.value]
        except:
            sys.exit(f"Runtime Error: Cannot read variable '{self.value}'")
        return None


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

