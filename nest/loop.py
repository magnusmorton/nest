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
import copy


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
    for loop in visitor.loop_environments:
        if loop.is_safe():
            safe_loops.append(loop)
    return safe_loops

    
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
        print("loops found %i" % len(self._loop_environments))
        return len(self._loop_environments)
        
    @property
    def loop_environments(self):
        return self._loop_environments
        
    def visit_For(self, node):
        top = False
        print(nest.affine_access.get_statements(node))
        if not self.current_loop_environment:
            self.current_loop_environment = LoopEnvironment(get_lower_bound(node.iter), get_upper_bound(node.iter), node.target.id, nest.affine_access.get_statements(node), node)
            top = True
            print("top")
        else:
            self.current_loop_environment.append_child(LoopEnvironment(get_lower_bound(node.iter),get_upper_bound(node.iter), node.target.id, nest.affine_access.get_statements(node), node))
        super(LoopVisitor, self).generic_visit(node)
        if top:
            self._loop_environments.append(self.current_loop_environment)
            self.current_loop_environment = None

class LoopEnvironment(object):
    

    CONST_KEY = 'const'
        
    def __init__(self,lower_bound=0,  upper_bound=0, target=None, statements=[], node=None):
        """ do something about this """
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._target = target
        self._child = None
        self._statements = statements
        self._node = node
        if self._statements:
            print(statements)
            for statement in self._statements:
                statement.loop_environment = self
                
    @property
    def tagged_node(self):
        return self._node
    
    
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
            return self._statements | self._child.all_statements
        else:
            return self._statements

    @property
    def node(self):
        """Returns the ast node this construct
        corresponds to
        
        Arguments:
        - `self`:
        """
        return self._node

    @property
    def non_locals(self):
        """
        Returns all non-local variables in loop
        Arguments:
        - `self`:
        """
        #for now, lets just assume the array statments are all there is.
        print("ALL STMTS")
        print(self.all_statements)
        return {stmt.target.id for stmt in self.all_statements}
        
    @property
    def lists(self):
        """
        Returns all non-local variables in loop
        Arguments:
        - `self`:
        """
        #for now, lets just assume the array statments are all there is.
        return [stmt.target for stmt in self.all_statements]
          
        
    def append_child(self, child):
        self._child = child
        
    def is_safe(self):
        # fix this!!!!
        safe = True
        print("All stmts:")
        print(self.all_statements)
        print("all stmts again")
        print(self.all_statements)
        statements_left = copy.deepcopy(self.all_statements)
        print("Statements left")
        print(statements_left)
        while statements_left:
            statement = statements_left.pop()
            print("hej")
            for other_statement in statements_left:
                print("hai")
                if nest.affine_access.is_dependent(statement, other_statement):
                    safe = False
        print(safe)
        return safe
        

