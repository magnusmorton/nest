'''
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
'''
import nest.loop
import ast
import unittest
from nest.tests.visitor_helper import VisitorHelper

SIMPLE_LOOP = """
for i in [1,2,3]:
    a = 1
"""

TWO_LOOPS = """
for i in [1,2,3]:
    a = 1

for num in [1,2,3]:
    a = num

"""

SIMPLE_NESTED = """
for a in [1,2,3]:
    for b in [4,5,6]:
        a*b
"""

SIMPLE_RANGE = """
for i in range(10):
    i*1
"""

SIMPLE_RANGE_5 = """
for i in range(5):
    i*1
"""

NESTED_RANGE = """
for i in range(5):
    for j in range(6):
        i*j
"""


NON_LOOP_STATEMENT = "print(a)"
    
class LoopVistitorTests(unittest.TestCase, VisitorHelper):
    '''A number of these tests are actually testing functionality tested elsewhere.  Should be changed'''
    
    def setUp(self):
        self.visitor = nest.loop.LoopVisitor()
        
    def test_1_loop_found(self):
        self.visit(SIMPLE_LOOP)
        self.assertEqual(self.visitor.loops_found, 1, "Only one loop should be found")
        
    def test_no_loops_found(self):
        self.visit(NON_LOOP_STATEMENT)
        self.assertEqual(self.visitor.loops_found, 0, "loops found when not present")
        
    def test_two_loops_found(self):
        self.visit(TWO_LOOPS)
        self.assertEqual(self.visitor.loops_found, 2, "Wrong number of loops found")
    
    def test_inner_loops_of_nest_ignored(self):
        self.visit(SIMPLE_NESTED)
        self.assertEqual(self.visitor.loops_found, 1, "Nested loop included in total number of loops")
    
    def test_nest_depth_is_0_when_no_nesting(self):
        self.visit(SIMPLE_LOOP)
        self.assertEqual(self.visitor.loop_environments[0].nesting_depth, 0, "Nesting detected when not present")
       
    def test_nest_depth_is_1_when_1_nested_loop(self):
        self.visit(SIMPLE_NESTED)
        self.assertEqual(self.visitor.loop_environments[0].nesting_depth, 1, "Wrong nesting depth detected")
       
    def test_upper_bound_found_when_range_10(self):
        self.visit(SIMPLE_RANGE)
        self.assertEqual(self.visitor.loop_environments[0].upper_bound, 9, "Detected upper bound was not 9")
                                            
    def test_upper_bound_found_when_range_5(self):
        self.visit(SIMPLE_RANGE_5)
        self.assertEqual(self.visitor.loop_environments[0].upper_bound, 4, "Detected upper bound was not 4")
        
    def test_upper_bound_found_in_inner_loop(self):
        self.visit(NESTED_RANGE)
        self.assertEqual(self.visitor.loop_environments[0].child.upper_bound, 5, "Detected upper bound was not 5")
                                            
    def test_target_found_in_simple_case(self):
        self.visit(SIMPLE_LOOP)
        self.assertEqual(self.visitor.loop_environments[0].target, "i", "Target found was not i")

    def test_target_found_when_name_not_i(self):
        self.visit(SIMPLE_NESTED)
        self.assertEqual(self.visitor.loop_environments[0].target, "a", "Target found was not a")
        
    def test_target_found_in_inner_loop(self):
        self.visit(SIMPLE_NESTED)
        self.assertEqual(self.visitor.loop_environments[0].child.target, "b", "Target found was not b")
        
        
class LoopEnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.env = nest.loop.LoopEnvironment()
    
    def test_unincreased_nest_level_is_0(self):
        assert self.env.nesting_depth == 0, "Nesting detected when not present"
        
    def test_append_child_adds_child(self):
        child = nest.loop.LoopEnvironment()
        self.env.append_child(child)
        self.assertEqual(self.env.child, child, "Child not found")

    def test_get_targets_single_nesting(self):
        env = nest.loop.LoopEnvironment(target="i")
        self.assertEqual(env.all_targets, ["i"], "targets found was not list containing i")

    def test_get_targets_multiple_nesting(self):
        env = nest.loop.LoopEnvironment(target="i")
        env.append_child(nest.loop.LoopEnvironment(target="j"))
        self.assertEqual(env.all_targets, ["i", "j"], "targets found was not list containing i, j only")

    
        
        
class BoundsTests(unittest.TestCase):
    
    ONE_TEN_RANGE = "range(1,10)"
    def test_get_upper_bound_returns_9_from_range(self):
        range_ast = ast.parse("range(10)")
        self.assertEqual(nest.loop.get_upper_bound(range_ast), 9, "Detected upper bound was not 9")
        
    def test_get_upper_bound_returns_4_from_range(self):
        range_ast = ast.parse("range(5)")
        self.assertEqual(nest.loop.get_upper_bound(range_ast), 4, "Detected upper bound was not 4")
        
    def test_get_lower_bound_returns_0_from_range(self):
        range_ast = ast.parse("range(5)")
        self.assertEqual(nest.loop.get_lower_bound(range_ast), 0, "Detected lower bound was not 0")
        
    def test_get_lower_bound_from_non_zero_start(self):
        range_ast = ast.parse(self.ONE_TEN_RANGE)
        self.assertEqual(nest.loop.get_lower_bound(range_ast), 1, "Detected lower bound was not 1")
        
    def test_get_upper_bound_from_two_arg_range(self):
        range_ast = ast.parse(self.ONE_TEN_RANGE)
        self.assertEqual(nest.loop.get_upper_bound(range_ast), 9, "Detected upper bound was not 9")
        

    