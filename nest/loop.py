import ast

def containsLoop(ast):
    loopVistor = LoopVistor()
    loopVistor.visit(ast)
    return False