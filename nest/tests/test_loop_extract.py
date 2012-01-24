import nest.loop
import ast
from nose import with_setup

LOOP = """for i in [1,2,3]:
    a = 1
"""

def setup():
    global simple_loop_ast 
    simple_loop_ast = ast.parse(LOOP)

def testFindLoop():
    assert nest.loop.containsLoop(simple_loop_as), "loop not found"