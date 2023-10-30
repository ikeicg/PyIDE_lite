import sys
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.curPos = -1
        self.curTok = None
        self.advance()

    def advance(self):
        self.curPos += 1
        if self.curPos < len(self.tokens):
            self.curTok = self.tokens[self.curPos]

    def runParse(self):
        statements = []
        # statements.append(self.isExpression())

        while self.curTok.type != "TT_EOF":

            if self.curTok.type == "TT_NWL":
                self.advance()
                continue

            statements.append(self.isExpression())

            if self.tokens[self.curPos].type != "TT_NWL":
                sys.exit("Parsing Error: expected newline")


        return statements

    def isStatement(self):
        pass

    def isExpression(self):
        return  self.BiOptn(self.isTerm, ["TT_PLUS", "TT_MINUS"])

    def isTerm(self):
        return  self.BiOptn(self.isFactor, ["TT_MULT", "TT_DIV"])

    def isFactor(self):
        tok = self.curTok

        if self.curTok.type == "TT_NUMBER":
            self.advance()
            return LfNode(tok)
        elif self.curTok.type == "TT_LPAREN":
            self.advance()
            expr = self.isExpression()
            if self.curTok.type == "TT_RPAREN":
                self.advance()
                return expr
            else:
                sys.exit("Parsing Error: Expected a )")
        elif self.curTok.type == "TT_EOF":
            return LfNode(tok)
        else:
            sys.exit("Parsing Error: Expected a number ")


    def BiOptn(self, func, opts):

        left = func()

        while self.curTok.type in opts:
            optn = self.curTok
            self.advance()
            right = func()
            left = BiOpNode(left, optn, right)

        return left

class LfNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok.value}'

    def read(self, obj):
        return self.tok.read(obj)

class BiOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'

    def read(self, obj):

        if self.op_tok.type == "TT_PLUS":
            return self.left_node.read(obj) + self.right_node.read(obj)
        if self.op_tok.type == "TT_MINUS":
            return self.left_node.read(obj) - self.right_node.read(obj)
        if self.op_tok.type == "TT_DIV":
            return self.left_node.read(obj) / self.right_node.read(obj)
        if self.op_tok.type == "TT_MULT":
            return self.left_node.read(obj) * self.right_node.read(obj)
