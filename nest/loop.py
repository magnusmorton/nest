import ast

def get_upper_bound(iterator):
    visitor = BoundsVisitor()
    visitor.visit(iterator)
    return visitor.upper_bound
    
    
class BoundsVisitor(ast.NodeVisitor):
    
    def __init__(self):
        super(BoundsVisitor, self ).__init__()
        self._upper_bound = None
    
    @property
    def upper_bound(self):
        """returns upper bound"""
        return self._upper_bound
    
    def visit_Call(self, node):
        if node.func.id == "range":
            self._upper_bound = node.args[0].n - 1

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
            self.current_loop_environment = LoopEnvironment(get_upper_bound(node.iter), node.target.id)
            top = True
        else:
            self.current_loop_environment.increase_nesting()
        super(LoopVisitor, self).generic_visit(node)
        if top:
            self._loop_environments.append(self.current_loop_environment)
            self.current_loop_environment = None

class LoopEnvironment(object):
    
    def __init__(self, bound, target=None):
        self._nesting_depth = 0
        self._upper_bound = bound
        self._target = target
    
    @property
    def nesting_depth(self):
        return self._nesting_depth
        
    def increase_nesting(self):
        self._nesting_depth += 1
        
    @property
    def upper_bound(self):
        return self._upper_bound

    @property
    def target(self):
        return self._target