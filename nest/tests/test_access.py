#!/usr/bin/env python
# encoding: utf-8
"""
test_access.py

Created by Magnus Morton on 2012-02-12.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import unittest
from nest.tests.visitor_helper import VisitorHelper

from nest.affine_access import *

class TestAccess(unittest.TestCase):
    def setUp(self):
        self.access = AffineAccess()
		
    def test_parameter_extracted(self):
        add_params(self.access, "i")
        self.assertTrue("i" in self.access.params)
	    
    def test_multiple_parameters_extractable(self):
        add_params(self.access, "i", "j")
        self.assertTrue("i" in self.access.params and "j" in self.access.params, "i and j are not both present")
	
    def test_implicit_coeff_extractable(self):
        add_params(self.access, "i")
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

def add_params(access, *params):
    for param in params:
        access.add_param(param)


class TestSubscriptVisitor(unittest.TestCase, VisitorHelper):
    
    SIMPLE_ACCESS = "[i]"
    TWO_ACCESS = "[i + j]"
    SIMPLE_COEFF = "[2*i]"
    TWO_COEFF    = "[2*i + 3*j]"
    SIMPLE_MINUS = "[-i]"

    def setUp(self):
        self.visitor = SubscriptVisitor()
        self.expected_access = AffineAccess()

    def test_simple_access_detected(self):
        self.visit(TestSubscriptVisitor.SIMPLE_ACCESS)
        add_params(self.expected_access, "i")
        self.assertEqual(self.visitor.access, self.expected_access, "detected access was not just 'i'")

    def test_two_paramater_access_detected(self):
        self.visit(TestSubscriptVisitor.TWO_ACCESS)
        add_params(self.expected_access, "i", "j")
        self.assertEqual(self.visitor.access, self.expected_access, "detected access was not just 'i' and 'j")
        
    def test_coeff_extract(self):
        self.visit(TestSubscriptVisitor.SIMPLE_COEFF)
        self.expected_access.add_param("i", 2)
        self.assertEqual(self.visitor.access, self.expected_access, "detected access did not have i with coeff of 2")
        
    def test_two_coeff_extract(self):
        self.visit(TestSubscriptVisitor.TWO_COEFF)
        self.expected_access.add_param("i", 2)
        self.expected_access.add_param("j", 3)
        self.assertEqual(self.visitor.access, self.expected_access, "both coefficients not extracted")
        
    def test_simple_minus(self):
        self.visit(TestSubscriptVisitor.SIMPLE_MINUS)
        self.expected_access.add_param("i", -1)
        assert self.visitor.access == self.expected_access, "negative coeff not extracted"

