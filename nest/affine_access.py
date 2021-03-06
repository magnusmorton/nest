"""
affine_access.py

Created by Magnus Morton on 2012-02-12.
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
"""
import ast
import copy
import py_pip

CONST_KEY = 'Zconst'
def get_statements(node):
    visitor = SubscriptVisitor()
    visitor.visit(node)
    print(visitor.accesses)
    return visitor.accesses

class SubscriptVisitor(ast.NodeVisitor):
    """
    This visits the index expression of an array access and
    extracts the coefficients of the loop index variables.
    It probably should be called something else.
    TODO: Symbolic Constants
    """
    
    CONST_KEY = 'Zconst'
    
    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = {}
        self._accesses = []
        self.in_subscript = False
        self.context = None

    @property
    def access(self):
        return self._access
        
    @property
    def accesses(self):
        return set(self._accesses)
        
    def visit_Subscript(self, node):
        target = node.value
        top = False
        if not self.in_subscript:
            self.in_subscript = True
            top = True
            self.context = node.ctx

        if isinstance(node.value, ast.Name):
            print(node.ctx)
            print(node.value.id + " should only be seen once")
            try:
                print("hellooooo!!!!!")
                self._accesses.append(Statement(node=node, access 
                                            =self.visit(node.slice), context=self.context))
            except:
                print("Affine error occurred")
            finally:
                print(self._accesses)
        else:
            self.generic_visit(node)

        if top:
            self.in_subscript = False
            self.context = None
            
        
    def visit_Index(self, node):
        self.in_subscript = True
        self._access = self.visit(node.value)
        self.in_subscript = False
        return self._access
        
    def visit_Name(self, node):
        return {node.id:1}
        
    def visit_Num(self, node):
        if isinstance(node.n, float):
            raise AffineError
        return {SubscriptVisitor.CONST_KEY: node.n}
          
    def visit_BinOp(self, node):
        if self.in_subscript:
            left_result = self.visit(node.left)
            right_result = self.visit(node.right)
            out = {}
            if isinstance(node.op,ast.Mult):
                if SubscriptVisitor.CONST_KEY in right_result:
                    right_result, left_result = left_result, right_result
                elif SubscriptVisitor.CONST_KEY not in left_result:
                    raise AffineError
                out =  dict_multiply(left_result[SubscriptVisitor.CONST_KEY],
                        right_result)
            elif isinstance(node.op, ast.Add):
                out =  dict_add(left_result, right_result)
            elif isinstance(node.op, ast.Sub):
                out = dict_add(left_result, dict_multiply(-1, right_result))
            else:
                raise AffineError
            return out
            
    def visit_UnaryOp(self, node):
        result = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return dict_multiply(-1, result)

class AffineError(Exception):
    """Thrown when the Access is not obviously affine"""
    pass
        
        
def dict_multiply(value, dictionary):
    return {k:value*v for k,v in dictionary.items() }
    
def dict_add(left, right):
    output = copy.deepcopy(left)
    for k,v in right.items():
        if k in output:
            output[k] += v
        else:
            output[k] = v
    return output
        
        
class Statement(object):
    (WRITE, READ) = range(2)
    
    def __init__(self, node=None, access=None, context=None):
        self._target = node.value
        self._access = access
        self._context = context
        self._id = id(node)
        self._loop_environment = None
        if isinstance(self._context, ast.Store):
            print("NO WAY!!!")
            self._context = Statement.WRITE
        if isinstance(self._context, ast.Load):
            self._context = Statement.READ


    @property
    def loop_environment(self):
        return self._loop_environment
        
    @loop_environment.setter
    def loop_environment(self, environment):
        self._loop_environment = environment            
    
    @property
    def target(self):
        return self._target
    
    @property
    def access(self):
        return self._access
        
    @property
    def context(self):
        return self._context

        
            
def constraint_normalize(*constraints):
    pass

def get_unique_keys(dict1, dict2):
    keys = []
    for key in dict1.keys():
        if key not in keys:
            keys.append(key)
    for key in dict2.keys():
        if key not in keys:
            keys.append(key)
    return keys

def is_dependent(stmt1, stmt2):
    """ This is a bit crazy"""
    if stmt1.context is Statement.READ and stmt2.context is Statement.READ:
        return False
    print(stmt1.access)
    print(stmt2.access)
    keys = get_unique_keys(stmt1.access, stmt2.access)
    print(keys)
    domain_matrix = []
    constraints = [0]
    # generate constraint array for access1 = access2
    for key in keys:
        if key == CONST_KEY:
            val1,val2 = 0,0
            if key in stmt1.access:
                val1 = stmt1.access[key]
            if key in stmt2.access:
                val2 = stmt2.access[key]
            constraints.append(val1 - val2)
        else:
            if key in stmt1.access:
                constraints.append(stmt1.access[key])
            else:
                constraints.append(0)
            if key in stmt2.access:
                constraints.append(stmt2.access[key])
            else:
                constraints.append(0)

    domain_matrix.append(constraints)
    constraints = [1]
    for key in keys:
            if key in stmt1.loop_environment.computed_bounds()[0]:
                constraints.append(stmt1.access[key])
            else:
                constraints.append(0)
            constraints.append(0)
    domain_matrix.append(constraints)
    print(domain_matrix)
    problem = py_pip.Problem(len(keys) -1)
    problem.domain = domain_matrix
    solution = problem.solve()
    print(solution.solution_exists)
    return solution.solution_exists


def generate_constraint_array(keys, constraints, access1, access2):
    for key in keys:
        if key == CONST_KEY:
            constraints.append(access1[key] - access2[key])
        else:
            if key in stmt1.access1:
                constraints.append(access1[key])
            else:
                constraints.append(0)
            if key in stmt2.access2:
                constraints.append(access2[key])
            else:
                constraints.append(0)


    

    
    

