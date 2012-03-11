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


# class TestSubscriptVisitor(unittest.TestCase, VisitorHelper):
#     
#     SIMPLE_ACCESS = "a[i]"
#     TWO_ACCESS = "a[i + j]"
#     SIMPLE_COEFF = "a[2*i]"
#     TWO_COEFF    = "a[2*i + 3*j]"
#     SIMPLE_MINUS = "a[-i]"
#     TWO_MINUS    = "a[i - j]"
#     SIMPLE_COEFF_MINUS = "a[-2*i]"
#     TWO_COEFF_MINUS    = "a[3*i - 2*j]"
# 
#     def setUp(self):
#         self.visitor = SubscriptVisitor()
# 
#     def test_simple_access_detected(self):
#         self.visit(TestSubscriptVisitor.SIMPLE_ACCESS)
#         self.assertEqual(self.visitor.access, {'i':1}, "detected access was not just 'i'")
# 
#     def test_two_paramater_access_detected(self):
#         self.visit(TestSubscriptVisitor.TWO_ACCESS)
#         self.assertEqual(self.visitor.access, {'i':1, 'j':1}, "detected access was not just 'i' and 'j")
#         
#     def test_coeff_extract(self):
#         self.visit(TestSubscriptVisitor.SIMPLE_COEFF)
#         self.assertEqual(self.visitor.access, {'i':2}, "detected access did not have i with coeff of 2")
#         
#     def test_two_coeff_extract(self):
#         self.visit(TestSubscriptVisitor.TWO_COEFF)
#         self.assertEqual(self.visitor.access, {'i':2, 'j':3}, "both coefficients not extracted")
#         
#     def test_simple_minus(self):
#         self.visit(TestSubscriptVisitor.SIMPLE_MINUS)
#         self.assertEqual(self.visitor.access,{'i':-1}, "negative coeff not extracted")
#         
#     def test_two_minus(self):
#         self.visit(TestSubscriptVisitor.TWO_MINUS)
#         self.assertEqual(self.visitor.access,{'i':1, 'j':-1}, "negative coeff of j not extracted")
#         
#     def test_simple_minus_with_coeff(self):
#         """tests extracting a negative coefficient"""
#         self.visit(TestSubscriptVisitor.SIMPLE_COEFF_MINUS)
#         self.assertEqual(self.visitor.access,{'i':-2}, "coeff of i not -2")
#     
#     def test__minus_with_two_coeff(self):
#         """tests extracting a negative coefficient"""
#         self.visit(TestSubscriptVisitor.TWO_COEFF_MINUS)
#         self.assertEqual(self.visitor.access,{'i':3, 'j':-2}, "coeff of j not -2")    
#         
class TestHelperMethods(unittest.TestCase):
    
    def test_dict_multiply(self):
        a = {'a':1, 'b':2}
        self.assertEqual({'a':2, 'b':4}, dict_multiply(2,a), "values not multiplied")
    
    def test_dict_multiply_three_elms_by_three(self):
        a = {'a':1, 'b':2, 'c':4}
        self.assertEqual({'a':3, 'b':6, 'c':12}, dict_multiply(3,a), "values not multiplied")
        
    def test_dict_add_simple(self):
        test_dict = {'a':1}
        self.assertEqual({'a':2}, dict_add(test_dict,test_dict),'a is not added to itself')
        
    def test_dict_add_two_keys(self):
        left = {'a':1, 'b':-2}
        right = {'a':3, 'b':1}
        self.assertEqual({'a':4, 'b':-1}, dict_add(left,right),'dicts not added correctly')
        

