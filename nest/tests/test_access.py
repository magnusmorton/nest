#!/usr/bin/env python
# encoding: utf-8
"""
test_access.py

Created by Magnus Morton on 2012-02-12.
(c) Copyright 2012 Magnus Morton. 

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


class TestSubscriptVisitor(unittest.TestCase, VisitorHelper):
    
    SIMPLE_ACCESS      = "a[i]"
    TWO_ACCESS         = "a[i + j]"
    SIMPLE_COEFF       = "a[2*i]"
    TWO_COEFF          = "a[2*i + 3*j]"
    SIMPLE_MINUS       = "a[-i]"
    TWO_MINUS          = "a[i - j]"
    SIMPLE_COEFF_MINUS = "a[-2*i]"
    TWO_COEFF_MINUS    = "a[3*i - 2*j]"
    DIV_ACCESS         = "a[i/2]"
    FLOAT_ACCESS       = "a[2.4354565767]"
    RIGHT_MULT         = "a[i*2]"
    SIMPLE_CONST       = "a[1]"
    CONST_EXPRESSION   = "a[i - 1]"
    NON_LINEAR         = "a[i*j]"
    ASSIGN = "a[i] = a[i+1]"

    def setUp(self):
        self.visitor = SubscriptVisitor()

    def test_simple_access_detected(self):
        self.visit(TestSubscriptVisitor.SIMPLE_ACCESS)
        self.assertEqual(self.visitor.access, {'i':1}, "detected access was not just 'i'")

    def test_two_paramater_access_detected(self):
        self.visit(TestSubscriptVisitor.TWO_ACCESS)
        self.assertEqual(self.visitor.access, {'i':1, 'j':1}, "detected access was not just 'i' and 'j")
        
    def test_coeff_extract(self):
        self.visit(TestSubscriptVisitor.SIMPLE_COEFF)
        self.assertEqual(self.visitor.access, {'i':2}, "detected access did not have i with coeff of 2")
        
    def test_two_coeff_extract(self):
        self.visit(TestSubscriptVisitor.TWO_COEFF)
        self.assertEqual(self.visitor.access, {'i':2, 'j':3}, "both coefficients not extracted")
        
    def test_simple_minus(self):
        self.visit(TestSubscriptVisitor.SIMPLE_MINUS)
        self.assertEqual(self.visitor.access,{'i':-1}, "negative coeff not extracted")
        
    def test_two_minus(self):
        self.visit(TestSubscriptVisitor.TWO_MINUS)
        self.assertEqual(self.visitor.access,{'i':1, 'j':-1}, "negative coeff of j not extracted")
        
    def test_simple_minus_with_coeff(self):
        """tests extracting a negative coefficient"""
        self.visit(TestSubscriptVisitor.SIMPLE_COEFF_MINUS)
        self.assertEqual(self.visitor.access,{'i':-2}, "coeff of i not -2")
    
    def test_minus_with_two_coeff(self):
        """tests extracting a negative coefficient"""
        self.visit(TestSubscriptVisitor.TWO_COEFF_MINUS)
        self.assertEqual(self.visitor.access,{'i':3, 'j':-2}, "coeff of j not -2")    
        
    # def test_div_access_throws_exception(self):
    #     with self.assertRaises(AffineError):
    #         self.visitBinOp(TestSubscriptVisitor.DIV_ACCESS)
            
    # def test_float_access_throws_exception(self):
    #     with self.assertRaises(AffineError):
    #         self.visitBinO(TestSubscriptVisitor.FLOAT_ACCESS)
            
    def test_right_mult(self):
        self.visit(TestSubscriptVisitor.RIGHT_MULT)
        self.assertEqual(self.visitor.access, {'i': 2}, "constant on right side of mult expression does not work")
       
    def test_const_extract(self):
        self.visit(TestSubscriptVisitor.SIMPLE_CONST)
        self.assertEqual(self.visitor.access, {SubscriptVisitor.CONST_KEY: 1}, "constant on right side of mult expression does not work")
        
    def test_const_expression(self):
        self.visit(TestSubscriptVisitor.CONST_EXPRESSION)
        self.assertEqual(self.visitor.access, {"i":1, SubscriptVisitor.CONST_KEY: -1}, "constant on right side of mult expression does not work")
        
    # def test_non_linear_access_throws_exception(self):
    #     with self.assertRaises(AffineError):
    #         self.visitBinOp(TestSubscriptVisitor.NON_LINEAR)
        
    
class TestStatement(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_if_context_is_Store_then_WRITE(self):
        stmt = Statement(context=ast.Store())
        self.assertEqual(stmt.context, Statement.WRITE, "context is not WRITE")
        
    def test_if_context_is_Load_then_READ(self):
        stmt = Statement(context=ast.Load())
        self.assertEqual(stmt.context, Statement.READ, "context is not READ")
                    
        
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
        
    def test_dict_add_dangling_left(self):
        left = {'a':1, 'b':1}
        right = {'a':1}
        self.assertEqual({'a':2, 'b':1}, dict_add(left,right),'dicts not added correctly')
        
    def test_dict_add_dangling_right(self):
        left = {'a':1, 'b':1}
        right = {'a':1, 'c':4}
        self.assertEqual({'a':2, 'b':1, 'c':4}, dict_add(left,right),'dicts not added correctly')
 
    # def test_normalize_two_constraints_simple(self):
    #     one = {'i':1}
    #     two = {'j'}

    def test_unique_keys(self):
        one = {'i':1}
        two = {'j':1}
        self.assertEqual(get_unique_keys(one, two), ['i', 'j'], "unique keys are not i & j")

    def test_unique_keys_obvious(self):
        one = {'i':1}
        two = {'i':1}
        self.assertEqual(get_unique_keys(one, two), ['i'], "unique keys are not just i")
    
        

