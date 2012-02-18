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
        self._access.add_param("i")

    @property
    def access(self):
        return self._access
        
        
    def visit_Name(self, node):
        self._access.add_param(node.id)



