"""
affine_access.py

Created by Magnus Morton on 2012-02-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
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

    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = AffineAccess()
        self._context = [None,None]

    @property
    def access(self):
        return self._access
        
    def visit_Name(self, node):
        self._access.add_param(node.id)
        self._context[0] = node.id
        
    def visit_Num(self, node):
        self._context[1] = node.n
        
    '''This will blow up when sym constants are involved!!!!'''    
    def visit_BinOp(self, node):
        coeff = 1
        self.generic_visit(node)
        if isinstance(node.op,ast.Mult):
            coeff = self._context[1]
        self._access.add_param(self._context[0], coeff)



