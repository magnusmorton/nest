import ast

test = """
import multiprocessing
pool = multiprocessing.Pool(4)

def fun():
    a = pool.apply_async(print, ["hola"])
    a.get()



fun()

"""

source = ast.parse(test)
print(ast.dump(source))

