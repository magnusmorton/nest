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
        super().__init__()

    def transform_tree(self):
        super().visit(self._tree)
        return self._tree

    def visit_For(self, node):
        for loop in self._loops:
            if node is loop.tagged_node:
                return 



def generate_parallel_function(loop):
    func = ast.FunctionDef()
    # need to generate random string here
    func.name = "placeholder"
    func.body = loop
    func.dectorator_list = []


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
        

        
        

    


