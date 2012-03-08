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
    
    (GENERIC,MULT, SUB, NEG) = range(4)

    def __init__(self):
        super(SubscriptVisitor, self).__init__()
        self._access = AffineAccess()
        self._context = 0
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
        if context == SubscriptVisitor.NEG or self._context == SubscriptVisitor.SUB: 
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
            self._context = SubscriptVisitor.MULT
        elif isinstance(node.op, ast.Sub):
            self._context_stack.append(SubscriptVisitor.SUB)
            self._context = SubscriptVisitor.SUB
        else:
            self._context_stack.append(SubscriptVisitor.GENERIC)
            self._context = SubscriptVisitor.GENERIC
        self.generic_visit(node)
        self._context_stack.pop()
        if self._foundID:
            self._access.add_param(self._foundID, self._found_const)
            
    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            self._context_stack.append(SubscriptVisitor.NEG)
            self._context = SubscriptVisitor.NEG
        self.generic_visit(node)
        self._context_stack.pop()
        if self._foundID:
            self._access.add_param(self._foundID, self._found_const)
        
        
        
            



