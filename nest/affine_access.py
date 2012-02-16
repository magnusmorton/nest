"""
affine_access.py

Created by Magnus Morton on 2012-02-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

class AffineAccess():
    
    def __init__(self):
        self._params = []
    
    def add_param(self, name):
        self._params += name
           
    @property
    def params(self):
        return self._params

    def get_coeff(self, param):
    	return 1
