"""
affine_access.py

Created by Magnus Morton on 2012-02-12.
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
"""
import ast

class AffineAccess():

    def __init__(self):
        self._params = {}

    def add_param(self, name, coeff=1):
        self._params[name] = coeff

    @property
    def params(self):
        return self._params

    def get_coeff(self, param):
    	return self._params[param]

    def __eq__(self, other):
        return self._params == other._params

class SubscriptVisitor(ast.NodeVisitor):
    
    (GENERIC,MULT, SUB, NEG) = range(4)

    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = AffineAccess()
        self._foundID = None
        self._context_stack = []

    @property
    def access(self):
        return self._access
        
    def visit_Name(self, node):
        context = None
        if self._context_stack:
            context = self._context_stack[len(self._context_stack)-1]
        self._access.add_param(node.id)
        if context == SubscriptVisitor.MULT:
            self._foundID = node.id
        if context == SubscriptVisitor.NEG: #or context == SubscriptVisitor.SUB: 
            self._foundID = node.id
            self._found_const = -1
        
    def visit_Num(self, node):
        if self._context_stack[len(self._context_stack)-1] == SubscriptVisitor.NEG:
            self._found_const = -node.n
        else:
            self._found_const = node.n
        
    '''This will blow up when sym constants are involved!!!! (Right now, constants too)'''    
    def visit_BinOp(self, node):
        if isinstance(node.op,ast.Mult):
            self._context_stack.append(SubscriptVisitor.MULT)
        elif isinstance(node.op, ast.Sub):
            self._context_stack.append(SubscriptVisitor.SUB)
            #self.visit(node.left)
        else:
            self._context_stack.append(SubscriptVisitor.GENERIC)
        self.generic_visit(node)
        self._context_stack.pop()
        if self._foundID:
            self._access.add_param(self._foundID, self._found_const)
            
    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            self._context_stack.append(SubscriptVisitor.NEG)
        self.generic_visit(node)
        self._context_stack.pop()
        if self._foundID:
            self._access.add_param(self._foundID, self._found_const)
        
        
def dict_multiply(value, dictionary):
    return {k:value*v for k,v in dictionary.items() }
    
def dict_add(left, right):
    output = {}
    for key in left.keys():
        if key in right:
            output[key] = left[key] + right[key] 
        else:
            output[key] = left[key]
    for key in right.keys():
        if key not in output:
            output[key] = right[key]
    return output
        
        
            



