"""
affine_access.py

Created by Magnus Morton on 2012-02-12.
Copyright (c) 2012 Magnus Morton. All rights reserved.
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
    
    (GENERIC,MULT, SUB) = range(3)

    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = AffineAccess()
        self._context = 0
        self._foundID = None

    @property
    def access(self):
        return self._access
        
    def visit_Name(self, node):
        self._access.add_param(node.id)
        if self._context == SubscriptVisitor.MULT:
            self._foundID = node.id
        if self._context == SubscriptVisitor.SUB:
            print("HELLO")
            self._foundID = node.id
            self._found_const = -1
        
    def visit_Num(self, node):
        self._found_const = node.n
        
    '''This will blow up when sym constants are involved!!!! (Right now, constants too)'''    
    def visit_BinOp(self, node):
        print(ast.dump(node))
        print(node.op)
        if isinstance(node.op,ast.Mult):
            self._context = SubscriptVisitor.MULT
        elif isinstance(node.op, ast.Sub):
            print("BLAH")
            self._context = SubscriptVisitor.SUB
        else:
            self._context = SubscriptVisitor.GENERIC
        self.generic_visit(node)
        if self._foundID:
            self._access.add_param(self._foundID, self._found_const)
            



