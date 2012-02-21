import ast

class VisitorHelper():
    def visit(self, source):
        self.visitor.visit(ast.parse(source))