#!/usr/bin/env python
# encoding: utf-8
"""
test_access.py

Created by Magnus Morton on 2012-02-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest

import nest.affine_access

class TestAccess(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_parameter_extracted(self):
	    access = nest.affine_access.AffineAccess()
	    access.add_param("i")
	    self.assertTrue("i" in access.params)
	    
	def test_multiple_parameters_extractable(self):
	    access = nest.affine_access.AffineAccess()
	    access.add_param("i")
	    access.add_param("j")
	    self.assertTrue("i" in access.params and "j" in access.params, "i and j are not both present")
    
if __name__ == '__main__':
	unittest.main()