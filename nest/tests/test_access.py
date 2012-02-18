#!/usr/bin/env python
# encoding: utf-8
"""
test_access.py

Created by Magnus Morton on 2012-02-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest

from nest.affine_access import *

class TestAccess(unittest.TestCase):
    def setUp(self):
        self.access = AffineAccess()
		
    def test_parameter_extracted(self):
        self.add_params("i")
        self.assertTrue("i" in self.access.params)
	    
    def test_multiple_parameters_extractable(self):
        self.add_params("i", "j")
        self.assertTrue("i" in self.access.params and "j" in self.access.params, "i and j are not both present")
	
    def test_implicit_coeff_extractable(self):
        self.add_params("i")
        self.assertEqual(self.access.get_coeff("i"), 1, "coeffecient of i is not 1")

    def test_explicit_coeff_extractable(self):
        self.access.add_param("i", 3)
        self.assertEqual(self.access.get_coeff("i"), 3, "coeffecient of i is not 3")

    def test_eq_true_when_equal(self):
        other_access = AffineAccess()
        self.access.add_param("i")
        other_access.add_param("i")
        self.assertEqual(self.access, other_access, "accesses not equal")

    def test_eq_false_when_not_equal(self):
        other_access = AffineAccess()
        self.access.add_param("i")
        other_access.add_param("j")
        self.assertNotEqual(self.access, other_access, "accesses equal")
	        
    def add_params(self, *params):
        for param in params:
            self.access.add_param(param)


class TestSubscriptVisitor(unittest.TestCase):
    
    SIMPLE_ACCESS = "[i]"
    TWO_ACCESS = "[i + j]"

    def setUp(self):
        pass

    def test_simple_access_detected(self):
        visitor = SubscriptVisitor()
        visitor.visit(ast.parse(TestSubscriptVisitor.SIMPLE_ACCESS))
        expected_access = AffineAccess()
        expected_access.add_param("i")
        self.assertEqual(visitor.access, expected_access, "detected access was not just 'i'")

    def test_two_paramater_access_detected(self):
        visitor = SubscriptVisitor()
        visitor.visit(ast.parse(TestSubscriptVisitor.TWO_ACCESS))
        expected_access = AffineAccess()
        expected_access.add_param("i")
        expected_access.add_param("j")
        self.assertEqual(visitor.access, expected_access, "detected access was not just 'i' and 'j")
	
    
if __name__ == '__main__':
	unittest.main()
