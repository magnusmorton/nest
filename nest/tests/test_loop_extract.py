import nest.loop
import ast
import unittest
from nose import with_setup

SIMPLE_LOOP = """for i in [1,2,3]:
    a = 1
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
        self.trivial_loop_ast = ast.parse(SIMPLE_LOOP)
        
        
    def test_1_loop_found(self):
        loop_visitor = nest.loop.LoopVisitor()
        loop_visitor.visit(self.trivial_loop_ast)
        self.assertEqual(loop_visitor.loops_found, 1, "Wrong number of loops found")
        
    def test_no_loops_found(self):
        loop_visitor = nest.loop.LoopVisitor()
        loop_visitor.visit(ast.parse(NON_LOOP_STATEMENT))
        self.assertEqual(loop_visitor.loops_found, 0, "loops found when not present")
        