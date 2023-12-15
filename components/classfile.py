import sys

class Error:
    def __init__(self, type, source, sourcePos, errPos, message):
        self.type = type
        self.source = source
        self.sourcePos = sourcePos
        self.errPos = errPos
        self.message = message

    def __repr__(self):
        return f'''{self.type}: Line {self.sourcePos}, Column {self.errPos}
            Source::        "{self.source}"
            Message::        {self.message}'''

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

    def gen_bytecode(self):
        return [f"LOAD_CONST:{self.value}"]


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

    def gen_bytecode(self):
        return [f"LOAD_NAME:{self.value}"]

class LfNode:
    def __init__(self, tok):
        self.tok = tok
        self.type = tok.value

    def __repr__(self):
        return f'{self.tok.value}'

    def read(self, obj):
        return self.tok.read(obj)

    def dfa(self):
        return [self.tok.value if isinstance(self.tok, IdentToken) else '']

    def gen_bytecode(self):
        return self.tok.gen_bytecode()

class BiOpNode:
    def __init__(self, left_node, op_tok, right_node, type="BiOpNode"):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.type = type

    def __repr__(self):
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'

    def read(self, obj):

        if self.op_tok.type == "TT_PLUS":
            return self.left_node.read(obj) + self.right_node.read(obj)
        if self.op_tok.type == "TT_MINUS":
            return self.left_node.read(obj) - self.right_node.read(obj)
        if self.op_tok.type == "TT_DIV":
            if self.right_node.read(obj) == 0:
                sys.exit("Runtime Error: Division by zero")
            return self.left_node.read(obj) / self.right_node.read(obj)
        if self.op_tok.type == "TT_MULT":
            return self.left_node.read(obj) * self.right_node.read(obj)
        if self.op_tok.type == "TT_POW":
            return self.left_node.read(obj) ** self.right_node.read(obj)

    def dfa(self):
        return self.left_node.dfa() + self.right_node.dfa()

    def gen_bytecode(self):
        if self.op_tok.type == "TT_PLUS":
            return self.left_node.gen_bytecode() + self.right_node.gen_bytecode() + ["BINARY_PLUS:0"]
        if self.op_tok.type == "TT_MINUS":
            return self.left_node.gen_bytecode() + self.right_node.gen_bytecode() + ["BINARY_MINUS:0"]
        if self.op_tok.type == "TT_DIV":
            return self.left_node.gen_bytecode() + self.right_node.gen_bytecode() + ["BINARY_DIV:0"]
        if self.op_tok.type == "TT_MULT":
            return self.left_node.gen_bytecode() + self.right_node.gen_bytecode() + ["BINARY_MULT:0"]
        if self.op_tok.type == "TT_POW":
            return  self.left_node.gen_bytecode() + self.right_node.gen_bytecode() + ["BINARY_POW:0"]

# Assign Statement
class AssignStmt:

    def __init__(self, ident, value):
        self.identifier = ident.value
        self.value = value

    def __repr__(self):
        return f"{self.identifier} = {self.value}"

    def dfa(self):
        return self.value.dfa()

    def gen_bytecode(self):
        return self.value.gen_bytecode() + [f"STORE_NAME:{self.identifier}"]

# Print Statement
class PrintStmt:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"print({self.value})"

    def dfa(self):
        return self.value.dfa()

    def gen_bytecode(self):
        return self.value.gen_bytecode() + [f"PRINT:0"]