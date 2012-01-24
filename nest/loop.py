import ast

def containsLoop(code):
    ast.parse(code)
    return False