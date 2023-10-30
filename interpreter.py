class Interpreter:

    def __init__(self, asts):
        self.asts = asts
        self.datastack = {}

    def execute(self):
        for ast in self.asts:
            print(ast.read(self))