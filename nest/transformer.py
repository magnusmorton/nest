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
import multiprocessing

try:
    cpus = multiprocessing.cpu_count()
except:
    cpus = 4


class ForTransformer(ast.NodeTransformer):
    RETURN_STUB = "nest_res"
    def __init__(self, abstract_tree, loops):
        self._tree = abstract_tree
        self._loops = loops
        self._functions = []
        try:
            self._cpus = multiprocessing.cpu_count()
        except:
            self._cpus = 4
        # generate functions for each parallel loop
        # for i,loop in enumerate(self._loops):
        #     
        
        super().__init__()

    def transform_tree(self):
        super().visit(self._tree)
        return self._tree

    def visit_Module(self, node):
        self.generic_visit(node)
        mp_import = """
import multiprocessing
pool = multiprocessing.pool(%i)
""" % self._cpus
        parsed_import = ast.Parse(mp_import)
        #append generated imports and functions
        return ast.Module(parsed_import.body + node.body + self._functions)
        
    def visit_For(self, node):
        for loop in self._loops:
            if node is loop.tagged_node:
                # generate call to generated function
                self._functions.append(generate_parallel_function(loop))
                slices = generate_slices(loop, cpus)
                arr_args = []
                for slc in slices:
                    arr_args.append([append_slice(name, slc) for name in loop.lists])
                stmts = []
                resnames  = []
                for i in range(cpus):
                    # generate call to apply_async
                    resname = "%s%i" % (ForTransformer.RETURN_STUB, i)
                    resnames.append(resnames)
                    fn_call = generate_function_call(id(loop), arr_args[i])
                    stmts.append(ast.Assign(targets=[ast.Name(id=resname,ctx=ast.Store())], value=fn_call))
                for i, arr in enumerate(loop.lists):
                    stmts.append(ast.parse(generate_template(resnames, i, arr)).body[0])
                return stmts
        else:
            self.generic_visit(node)

def generate_template(resnames, i, arr):
    template = "%(name)s =[ "
    for i,name in enumerate(resnames):
        if i < len(resnames-1):
            template += name + ".get()[%(index)d] +"
        else:
            template += name + ".get()[%(index)d]]"
    return template % {name:arr, index:i}

def append_slice(name, slice_pair):
    return "%s[%i:%i]" % (name, slice_pair[0], slice_pair[1])
    
def generate_slices(loop, cpu_count):
    """
    """
    start = loop.lower_bound
    end  = loop.upper_bound
    size = end - start
    slice_size = size // cpu_count
    slices = []
    for i in range(cpu_count):
        if i == cpu_count - 1:
            slices.append((i*slice_size, end))
        else:
            slices.append((i*slice_size, slice_size* i + slice_size))

    
    return slices

def slice_size(loop):
    return loop.upper_bound // cpus

class BoundsTransformer(ast.NodeTransformer):

    def __init__(self,loop):
        self.loop = loop
        self.top_level = False
        

    def visit_For(self, node):
        if not self.top_level:
            self.top_level = True
            self.generic_visit(node)
        self.top_level = False
        
    
    def visit_Call(self, node):
        if node.func.id = "range":
            # this needs to be changed at some point
            node.args[0] = slice_size(self.loop)
            return node
        else:
            self.generic_visit(node)
            
            


def generate_parallel_function(loop):
    # need to generate random string here
    name = "nest_fn" + id(loop)
    args = []
    for arg in loop.non_locals:
        arg_name = ast.Name(arg, ast.Param())
        args.append(arg_name)
    args = ast.arguments(args=args, varag=None, kwarg=None, defaults=[])
    return_values = (ast.parse(str(loop.non_locals))).body[0]
    body = [loop.node, return_values]
    dectorator_list = []
    return ast.FunctionDef(name=name, args=args, body=body, decorator_list=[])


def generate_function_call(node_id, arr_args):
    parsed_call = ast.parse("pool.apply_async(nest_fn%d)" % node_id)
    call = ast.Call()
    call.func = ast.Attribute(value=Name(id="pool", ctx=ast.Load()), attr="apply_async", ctx=ast.Load())
    call.func.id = "nest_fn" + node_id 
    call.func.ctx = ast.Load()
    parsed_args = ast.parse(str(arr_args))
    call.args = [ast.Name(id="nest_fn%i" % node_id, ctx=ast.Load), parsed_args.body[0]]
    call.keywords = []
    call.starargs = None
    call.kwargs = None
    return call
        

        
        

    


