import ast

def containsLoop(ast):
    loopVistor = LoopVistor()
    loopVistor.visit(ast)
    return False
    
    
class LoopVisitor(ast.NodeVisitor):
    
    def __init__(self):
        super(LoopVisitor, self).__init__()
        self._loops_found = 0
    
    @property    
    def loops_found(self):
        return self._loops_found
        
    def visit_For(self, node):
        self._loops_found += 1