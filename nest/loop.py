import ast
    
class LoopVisitor(ast.NodeVisitor):
    
    def __init__(self):
        super(LoopVisitor, self).__init__()
        self._loop_environments = []
        self.current_loop_environment = None
    
    @property    
    def loops_found(self):
        return len(self._loop_environments)
        
    @property
    def loop_environments(self):
        return self._loop_environments
        
    def visit_For(self, node):
        top = False
        if not self.current_loop_environment:
            self.current_loop_environment = LoopEnvironment()
            top = True
        else:
            self.current_loop_environment.increase_nesting()
        super(LoopVisitor, self).generic_visit(node)
        if top:
            self._loop_environments.append(self.current_loop_environment)
            self.current_loop_environment = None

class LoopEnvironment(object):
    
    def __init__(self):
        self._nesting_depth = 0
    
    @property
    def nesting_depth(self):
        return self._nesting_depth
        
    def increase_nesting(self):
        self._nesting_depth += 1
    