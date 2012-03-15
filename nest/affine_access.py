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

def get_statements(node):
    visitor = SubscriptVisitor()
    visitor.visit(node)
    return visitor.accesses

class SubscriptVisitor(ast.NodeVisitor):
    """
    This visits the index expression of an array access and
    extracts the coefficients of the loop index variables.
    It probably should be called something else.
    TODO: Symbolic Constants
    """
    
    CONST_KEY = 'const'
    
    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = {}
        self._accesses = []
        self.in_subscript = False

    @property
    def access(self):
        return self._access
        
    @property
    def accesses(self):
        return self._accesses
        
    def visit_Subscript(self, node):
        target = node.value
        print(node.ctx)
        try:
            self.accesses.append(Statement(target=target, access =self.visit(node.slice), context = node.ctx))
        except:
            pass
        finally:
            pass
        
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
    
    def __init__(self, target=None, access=None, context=None):
        self._target = target
        self._access = access
        self._context = None
        self._loop_environment = None
        if isinstance(context, ast.Store):
            self._context = Statement.WRITE
        if isinstance(context, ast.Load):
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

def is_dependent(stmt1, stmt2):
    if stmt1.context is Statement.READ and stmt2.context is Statement.READ:
        return False
    domain = []
    

    
    

