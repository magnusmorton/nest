#!/usr/bin/env python
# encoding: utf-8
"""
test_access.py

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
    TWO_MINUS    = "[i - j]"
    SIMPLE_COEFF_MINUS = "[-2*i]"
    TWO_COEFF_MINUS    = "[3*i - 2*j]"

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
        self.assertEqual(self.visitor.access,self.expected_access, "negative coeff not extracted")
        
    def test_two_minus(self):
        return  #not yet implemented
        self.visit(TestSubscriptVisitor.TWO_MINUS)
        self.expected_access.add_param("i")
        self.expected_access.add_param("j", -1)
        self.assertEqual(self.visitor.access,self.expected_access, "negative coeff of j not extracted")
        
    def test_simple_minus_with_coeff(self):
        """tests extracting a negative coefficient"""
        self.visit(TestSubscriptVisitor.SIMPLE_COEFF_MINUS)
        self.expected_access.add_param("i", -2)
        self.assertEqual(self.visitor.access,self.expected_access, "coeff of i not -2")
    
    def test__minus_with_two_coeff(self):
        """tests extracting a negative coefficient"""
        return #not yet implemented
        self.visit(TestSubscriptVisitor.TWO_COEFF_MINUS)
        self.expected_access.add_param("i", 3)
        self.expected_access.add_param("j", -2)
        self.assertEqual(self.visitor.access,self.expected_access, "coeff of j not -2")    
        
class TestHelperMethods(unittest.TestCase):
    
    def test_dict_multiply(self):
        a = {'a':1, 'b':2}
        self.assertEqual({'a':2, 'b':4}, dict_multiply(2,a), "values not multiplied")
    
    def test_dict_multiply_three_elms_by_three(self):
        a = {'a':1, 'b':2, 'c':4}
        self.assertEqual({'a':3, 'b':6, 'c':12}, dict_multiply(3,a), "values not multiplied")

