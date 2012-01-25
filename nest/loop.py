import ast

def containsLoop(ast):
    loopVistor = LoopVistor()
    loopVistor.visit(ast)
    return False
    
    
class LoopVisitor(ast.NodeVisitor):
    
    def __init__(self):
        super(LoopVisitor, self).__init__()
        self._loops_found = 0
        self._loop_environments = []
        self._in_loop = False
    
    @property    
    def loops_found(self):
        return len(self._loop_environments)
        
    @property
    def loop_environments(self):
        return self._loop_environments
        
    def visit_For(self, node):
        top = False
        if not self._in_loop:
            self._loops_found += 1
            self._loop_environments.append(LoopEnvironment())
            self._in_loop = True
            top = True
        self.generic_visit(node)
        if top:
            self._in_loop = False

class LoopEnvironment(object):
    
    @property
    def nesting_depth(self):
        return 0