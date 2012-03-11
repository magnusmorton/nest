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
import copy


class SubscriptVisitor(ast.NodeVisitor):
    
    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = {}

    @property
    def access(self):
        return self._access
        
    def visit_Index(self, node):
        self._access = self.visit(node.value)
        
    def visit_Name(self, node):
        return {node.id:1}
        
    def visit_Num(self, node):
        if isinstance(node.n, float):
            raise AffineError
        return {'const': node.n}
          
    def visit_BinOp(self, node):
        left_result = self.visit(node.left)
        right_result = self.visit(node.right)
        if isinstance(node.op,ast.Mult):
            return dict_multiply(left_result['const'], right_result)
        elif isinstance(node.op, ast.Add):
            return dict_add(left_result, right_result)
        elif isinstance(node.op, ast.Sub):
            return dict_add(left_result, dict_multiply(-1, right_result))
        else:
            raise AffineError
            
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
        
        
            



