import nest.loop
import ast
import unittest
from nose import with_setup

LOOP = """for i in [1,2,3]:
    a = 1
"""

""" Ignore these first tests.  They were included when I was trying to figure out what to do.
"""
def setup():
    global simple_loop_ast 
    simple_loop_ast = ast.parse(LOOP)

def testFindLoop():
    assert nest.loop.containsLoop(simple_loop_as), "loop not found"
    
class LoopVistitorTests(unittest.TestCase):
    def setUp(self):
        self.trivial_loop_ast = ast.parse(LOOP)
        
        
    def test1LoopFound(self):
        loopVisitor = nest.loop.LoopVisitor()
        loopVisitor.visit(trivial_loop_ast)
        assert loopVistor.loopsFound() == 1, "Wrong number of loops found"