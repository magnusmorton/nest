import nest.loop
import ast
import unittest
from nose import with_setup

SIMPLE_LOOP = """for i in [1,2,3]:
    a = 1
"""

TWO_LOOPS = """for i in [1,2,3]:
    a = 1

for num in [1,2,3]:
    a = num

"""


NON_LOOP_STATEMENT = "print(a)"

""" Ignore these first tests.  They were included when I was trying to figure out what to do.
"""
def setup():
    global simple_loop_ast 
    simple_loop_ast = ast.parse(SIMPLE_LOOP)

def testFindLoop():
    assert nest.loop.containsLoop(simple_loop_as), "loop not found"
    
class LoopVistitorTests(unittest.TestCase):
    def setUp(self):
        self.loop_visitor = nest.loop.LoopVisitor()
        
    def test_1_loop_found(self):
        self.loop_visitor.visit(ast.parse(SIMPLE_LOOP))
        self.assertEqual(self.loop_visitor.loops_found, 1, "Only one loop should be found")
        
    def test_no_loops_found(self):
        self.loop_visitor.visit(ast.parse(NON_LOOP_STATEMENT))
        self.assertEqual(self.loop_visitor.loops_found, 0, "loops found when not present")
        
    def test_two_loops_found(self):
        self.loop_visitor.visit(ast.parse(TWO_LOOPS))
        self.assertEqual(self.loop_visitor.loops_found, 2, "Wrong number of loops found")
        
        