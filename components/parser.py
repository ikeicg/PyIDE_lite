from PyIDE_lite.components.classfile import *

class Parser:

    def __init__(self, source, tokens, sourcePos):
        self.source = source
        self.tokens = tokens
        self.curPos = -1
        self.curTok = None
        self.sourcePos = sourcePos
        self.errors = []
        self.advance()

    def advance(self):
        self.curPos += 1
        if self.curPos < len(self.tokens):
            self.curTok = self.tokens[self.curPos]

    def parseTokens(self):

        if self.curTok.type == "TT_EOF":
            return [None, None]

        while self.curTok.type != "TT_EOF":

            if self.curTok.type == "TT_NWL":
                self.advance()
                continue

            statement = self.isStatement()

            if (len(self.errors) > 0):
                return [None, self.errors]
            else:
                if(self.tokens[self.curPos].type != "TT_EOF"):
                    tok = self.tokens[self.curPos]
                    return [None, [Error("Parsing Error", self.source,
                                         self.sourcePos, tok.start, "Expected Newline")]]
                return [statement, None]

    def isStatement(self):

        if self.curTok.type == "TT_IDENT":  # assignment statement
            identifier = self.curTok
            self.advance()
            if self.curTok.type == "TT_EQ":
                self.advance()
                expression = self.isexpression()
                return AssignStmt(identifier, expression)
            else:
                message = " Invalid Statement expected an '=' "
                self.errors.append(Error("Parsing Error", self.source, self.sourcePos, self.curTok.start, message))
        elif self.curTok.type == "TT_KEYW" and self.curTok.value == "print":  # print statement
            self.advance()
            if self.curTok.type == "TT_LPAREN":
                self.advance()
                expression = self.isexpression()

                if self.curTok.type == "TT_RPAREN":
                    self.advance()
                    return PrintStmt(expression)
                else:
                    message = "expected ')' "
                    self.errors.append(Error("Parsing Error", self.source, self.sourcePos, self.curTok.start, message))
            else:
                # sys.exit("Parsing Error: expected '(' ")
                message = "expected '('"
                self.errors.append(Error("Parsing Error", self.source, self.sourcePos, self.curTok.start, message))
        else:
            message = "Invalid Statement Line"
            self.errors.append(Error("Parsing Error", self.source, self.sourcePos, self.curTok.start, message))

    def isexpression(self):
        return self.formBiOp(self.isterm, ["TT_PLUS", "TT_MINUS"])

    def isterm(self):
        return self.formBiOp(self.ispower, ["TT_MULT", "TT_DIV"])

    def ispower(self):
        return self.formBiOp(self.isprimary, ["TT_POW"])

    def isprimary(self):

        tok = self.curTok

        if self.curTok.type == "TT_NUMBER":
            self.advance()
            expr = LfNode(tok)
        elif self.curTok.type == "TT_IDENT":
            self.advance()
            expr = LfNode(tok)
        elif (self.curTok.type == "TT_KEYW" and self.curTok.value == "memory"):
            self.advance()
            expr = LfNode(tok)
        elif self.curTok.type == "TT_LPAREN":
            self.advance()
            expr = self.isexpression()
            if self.curTok.type == "TT_RPAREN":
                self.advance()
            else:
                message = "Expected a )"
                self.errors.append(Error("Parsing Error", self.source, self.sourcePos, self.curTok.start, message))
        else:
            expr = ""
            message = f"Expected an expression, but got '{tok.type}'"
            self.errors.append(
                Error("Parsing Error", self.source, self.sourcePos, self.tokens[self.curPos].end, message))

        return expr

    def formBiOp(self,  func, opts):

        left = func()

        while self.curTok.type in opts:
            optn = self.curTok
            self.advance()
            right = func()
            left = BiOpNode(left, optn, right)

        return left