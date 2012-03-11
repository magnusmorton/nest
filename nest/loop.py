'''
(c) Copyright 2012 Magnus Morton. All Rights Reserved. 

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


"""These methods should go somewhere else"""
def get_upper_bound(iterator):
    visitor = BoundsVisitor()
    visitor.visit(iterator)
    return visitor.upper_bound
    
def get_lower_bound(iterator):
    visitor = BoundsVisitor()
    visitor.visit(iterator)
    return visitor.lower_bound
    
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
            self.current_loop_environment = LoopEnvironment(get_upper_bound(node.iter), node.target.id)
            top = True
        else:
            self.current_loop_environment.append_child(LoopEnvironment(get_upper_bound(node.iter), node.target.id))
        super(LoopVisitor, self).generic_visit(node)
        if top:
            self._loop_environments.append(self.current_loop_environment)
            self.current_loop_environment = None

class LoopEnvironment(object):
    
    def __init__(self, bound=0, target=None):
        self._upper_bound = bound
        self._target = target
        self._child = None
    
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
    def target(self):
        return self._target

    @property
    def all_targets(self):
        if self._child is None:
            return [self._target]
        else:
            return  [self._target] + self._child.all_targets
    
    @property
    def child(self):
        return self._child
        
    def append_child(self, child):
        self._child = child
        