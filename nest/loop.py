'''
(c) Copyright 2012 Magnus Morton.

This file is part of Nest.

Nest is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Nest.  If not, see <http://www.gnu.org/licenses/>.
'''
import ast
import nest.affine_access


"""These methods should go somewhere else"""
def get_upper_bound(iterator):
    visitor = BoundsVisitor()
    visitor.visit(iterator)
    return visitor.upper_bound
    
def get_lower_bound(iterator):
    visitor = BoundsVisitor()
    visitor.visit(iterator)
    return visitor.lower_bound

def get_safe_loops(parsed_ast):
    visitor = LoopVisitor()
    visitor.visit(parsed_ast)
    safe_loops = []
    # reduce number of comparisons here
    for loop in visitor.loops_found:
        if loop.is_safe:
            safe_loops.append(loop)

    
class BoundsVisitor(ast.NodeVisitor):
    
    def __init__(self):
        super(BoundsVisitor, self ).__init__()
        self._upper_bound = None
        self._lower_bound = None
    
    @property
    def upper_bound(self):
        """returns upper bound"""
        return self._upper_bound
        
    @property
    def lower_bound(self):
        """returns the lower bound of the iterator"""
        return self._lower_bound
    
    def visit_Call(self, node):
        if node.func.id == "range":
            if len(node.args) > 1:
                self._lower_bound = node.args[0].n
                self._upper_bound = node.args[1].n -1
            else:
                self._lower_bound = 0
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
            self.current_loop_environment = LoopEnvironment(get_lower_bound(node.iter), get_upper_bound(node.iter), node.target.id, nest.affine_access.get_statements(node))
            top = True
        else:
            self.current_loop_environment.append_child(LoopEnvironment(get_lower_bound(node.iter),get_upper_bound(node.iter), node.target.id, nest.affine_access.get_statements(node)))
        super(LoopVisitor, self).generic_visit(node)
        if top:
            self._loop_environments.append(self.current_loop_environment)
            self.current_loop_environment = None

class LoopEnvironment(object):
    

    CONST_KEY = 'const'
        
    def __init__(self,lower_bound=0,  upper_bound=0, target=None, statements=[]):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._target = target
        self._child = None
        self._statements = statements
        if self._statements:
            for statement in self._statements:
                statement.loop_environment = self
    
    @property
    def nesting_depth(self):
        if not self._child:
            return 0
        else:
            return 1 + self._child.nesting_depth
        
    @property
    def upper_bound(self):
        return self._upper_bound
        
    @property
    def lower_bound(self):
        return self._lower_bound

    @property
    def target(self):
        return self._target

    def computed_bounds(self):
        #TODO: FM Stuff should go here
        output = []
        #lower
        output.append({self._target:1, LoopEnvironment.CONST_KEY: -1*self._lower_bound})
        #upper
        output.append({self._target:-1, LoopEnvironment.CONST_KEY: self._upper_bound})
        return output

    @property
    def all_targets(self):
        if self._child is None:
            return [self._target]
        else:
            return [self._target] + self._child.all_targets
    
    @property
    def child(self):
        return self._child

    @property
    def all_statements(self):
        if self._child:
            return self._statements + self._child.all_statements
        else:
            return self._statements
        
    def append_child(self, child):
        self._child = child
        
    def is_safe(self):
        safe = True
        statements_left = self.all_statements
        while statements_left:
            statement = statements_left.pop()
            for other_statement in statements_left:
                if nest.affine_access.is_dependent(statement, other_statement):
                    safe = False
        return safe
        

