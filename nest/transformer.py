'''
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
'''
import ast

class ForTransformer(ast.NodeTransformer):

    def __init__(self, abstract_tree, loops):
        self._tree = abstract_tree
        self._loops = loops
        self._functions = []

        # generate functions for each parallel loop
        for i,loop in enumerate(self._loops):
            self._functions.append(generate_parallel_function(i,loop))
            
        super().__init__()

    def transform_tree(self):
        super().visit(self._tree)
        return self._tree

    def visit_Module(self, node):
        self.generic_visit(node)
        mp_import = """
import multiprocessing
pool = multiprocessing.pool(4)
"""
        parsed_import = ast.Parse(mp_import)
        return ast.Module(parsed_import.body + node.body + self._functions)
        
    def visit_For(self, node):
        for loop in self._loops:
            if node is loop.tagged_node:
                return 



def generate_parallel_function(count, loop):
    # need to generate random string here
    name = "placeholder" + count
    args = []
    for arg in loop.non_locals:
        arg_name = ast.Name(arg, ast.Param())
        args.append(arg_name)
    args = ast.arguments(args=args, varag=None, kwarg=None, defaults=[])
    #func.body = loop
    dectorator_list = []
    return ast.FunctionDef(name=name, args=args, body=[loop], decorator_list=[])


def generate_function_call(loop_name):
    call = ast.Call()
    call.func = ast.Name()
    call.func.id = loop_name
    call.func.ctx = ast.Load()
    call.args = []
    call.keywords = []
    call.starargs = None
    call.kwargs = None
    return call
        

        
        

    


