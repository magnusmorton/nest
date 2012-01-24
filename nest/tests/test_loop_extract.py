import nest.loop

LOOP = """for i in [1,2,3]:
    a = 1
"""

def testFindLoop():
    assert nest.loop.containsLoop(LOOP), "loop not found"