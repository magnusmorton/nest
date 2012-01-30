import nest.loop
import ast
import unittest

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


NON_LOOP_STATEMENT = "print(a)"
    
class LoopVistitorTests(unittest.TestCase):
    def setUp(self):
        self.loop_visitor = nest.loop.LoopVisitor()
        
    def test_1_loop_found(self):
        self.visit(SIMPLE_LOOP)
        self.assertEqual(self.loop_visitor.loops_found, 1, "Only one loop should be found")
        
    def test_no_loops_found(self):
        self.visit(NON_LOOP_STATEMENT)
        self.assertEqual(self.loop_visitor.loops_found, 0, "loops found when not present")
        
    def test_two_loops_found(self):
        self.visit(TWO_LOOPS)
        self.assertEqual(self.loop_visitor.loops_found, 2, "Wrong number of loops found")
    
    def test_inner_loops_of_nest_ignored(self):
        self.visit(SIMPLE_NESTED)
        self.assertEqual(self.loop_visitor.loops_found, 1, "Nested loop included in total number of loops")
    
    def test_nest_depth_is_0_when_no_nesting(self):
        self.visit(SIMPLE_LOOP)
        self.assertEqual(self.loop_visitor.loop_environments[0].nesting_depth, 0, "Nesting detected when not present")
       
    def test_nest_depth_is_1_when_1_nested_loop(self):
        self.visit(SIMPLE_NESTED)
        self.assertEqual(self.loop_visitor.loop_environments[0].nesting_depth, 1, "Wrong nesting depth detected")
       # 
       # def test_upper_bound_found_when_range_10(self):
       #     self.loop_visitor
       
    def visit(self, source):
        self.loop_visitor.visit(ast.parse(source))
        
class LoopEnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.env = nest.loop.LoopEnvironment()
    
    def test_single_increased_nesting(self):
        self.env.increase_nesting()
        assert self.env.nesting_depth == 1, "Wrong nesting depth detected"
        
    def test_unincreased_nest_level_is_0(self):
        assert self.env.nesting_depth == 0, "Nesting detected when not present"
        
        
    