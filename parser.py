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

        while self.curTok.type != "TT_EOF":

            if self.curTok.type == "TT_NWL":
                self.advance()
                continue

            statement = self.isStatement()
            if statement:
                statements.append(statement)
            else:
                sys.exit("Parsing Error: invalid statement line")

            if self.tokens[self.curPos].type != "TT_NWL":
                sys.exit("Parsing Error: expected newline")


        return statements

    def isStatement(self):

        if self.curTok.type == "TT_IDENT":  # assignment statement
            identifier = self.curTok
            self.advance()
            if self.curTok.type == "TT_EQ":
                self.advance()
                expression = self.isExpression()
                return AssignStmt(identifier, expression)
        elif self.curTok.type == "TT_KEYW" and self.curTok.value == "print":  # print statement
            self.advance()
            if self.curTok.type == "TT_LPAREN":
                self.advance()
                expression = self.isExpression()

                if self.curTok.type == "TT_RPAREN":
                    self.advance()
                    return PrintStmt(expression)
                else:
                    sys.exit("Parsing Error: expected ')' ")
            else:
                sys.exit("Parsing Error: expected '(' ")


    def isExpression(self):
        return  self.BiOptn(self.isTerm, ["TT_PLUS", "TT_MINUS"])

    def isTerm(self):
        return  self.BiOptn(self.isExponent, ["TT_MULT", "TT_DIV"])

    def isExponent(self):
        return self.BiOptn(self.isFactor, ["TT_POW"])

    def isFactor(self):
        tok = self.curTok
        # print("test1", tok)

        if self.curTok.type == "TT_NUMBER":
            self.advance()
            return LfNode(tok)
        elif self.curTok.type == "TT_IDENT":
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
            sys.exit("Parsing Error: Expected a number, but got")


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
        if self.op_tok.type == "TT_POW":
            return self.left_node.read(obj) ** self.right_node.read(obj)

# Assign Statement
class AssignStmt:

    def __init__(self, ident, value):
        self.identifier = ident.value
        self.value = value

    def __repr__(self):
        return f"{self.identifier} = {self.value}"

    def read(self, obj):
        obj.datastack[self.identifier] = self.value.read(obj)

# Print Statement
class PrintStmt:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"print({self.value})"

    def read(self, obj):
         print(self.value.read(obj))
