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
        # mp_import = """
# import multiprocessing
# pool = multiprocessing.Pool(%i)
# """ % cpus
#         parsed_import = ast.parse(mp_import)
        parsed_import = ast.Import(names=[ast.alias(name='multiprocessing', asname=None)])
       # parsed_pool = ast.Assign(targets=[ast.Name(id='pool', ctx=ast.Store())], value=ast.Call(func=ast.Attribute(value=ast.Name(id='multiprocessing', ctx=ast.Load()), attr='Pool', ctx=ast.Load()), args=[ast.Num(n=cpus)], keywords=[], starargs=None, kwargs=None))
        #append generated imports and functions
#        ast.fix_missing_locations(self._tree)
        return_module = ast.Module(body = [parsed_import]  + self._functions + self._tree.body)
        return return_module
    
    def visit_Call(self, node):
        self.generic_visit(node)
        return ast.increment_lineno(node, 1000)
    # def visit_Module(self, node):
    #         self.generic_visit(node)
    #         mp_import = """
    # import multiprocessing
    # pool = multiprocessing.pool(%i)
    # """ % self._cpus
    #         parsed_import = ast.parse(mp_import)
    #         #append generated imports and functions
    #         print(parsed_import.body)
    #         return None
    #         return ast.Module(body = [parsed_import.body + node.body + self._functions])
        
    def visit_For(self, node):
        for loop in self._loops:
            print(loop.tagged_node)
            if node is loop.tagged_node:
                # generate call to generated function
                self._functions.append(generate_parallel_function(loop))
                slices = generate_slices(loop, cpus)
                arr_args = []
                for slc in slices:
                    arr_args.append([append_slice(name.id, slc) for name in loop.lists])
                stmts = []
                parsed_import = ast.Import(names=[ast.alias(name='multiprocessing', asname=None)])
                parsed_pool = ast.Assign(targets=[ast.Name(id='pool', ctx=ast.Store())], value=ast.Call(func=ast.Attribute(value=ast.Name(id='multiprocessing', ctx=ast.Load()), attr='Pool', ctx=ast.Load()), args=[ast.Num(n=cpus)], keywords=[], starargs=None, kwargs=None))
                # stmts.append(parsed_import)
                stmts.append(parsed_pool)
                resnames  = []
                for i in range(cpus):
                    # generate call to apply_async
                    resname = "%s%i" % (ForTransformer.RETURN_STUB, i)
                    resnames.append(resname)
                    fn_call = generate_function_call(id(loop), arr_args[i], i)
                    stmts.append(ast.Assign(targets=[ast.Name(id=resname,ctx=ast.Store())], value=fn_call))
                for i, arr in enumerate(loop.lists):
                    print("lists %i" % i)
                    stmts.append(ast.parse(generate_template(resnames, i, arr)).body[0])
                    
                return stmts
        else:
            print("HELLOOO!!!")
            self.generic_visit(node)

def generate_template(resnames, index, arr):
    template = "%(name)s = "
    for i,name in enumerate(resnames):
        if i < len(resnames) -1:
            template += name + ".get()[%(index)d] +"
        else:
            template += name + ".get()[%(index)d]"
    print(template)
    return template % {'name':arr.id, 'index':index}

def append_slice(name, slice_pair):
    return "%s[%i:%i]" % (name, slice_pair[0], slice_pair[1])
    
def generate_slices(loop, cpu_count):
    """
    """
    start = loop.lower_bound
    end  = loop.upper_bound +1
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
    return (loop.upper_bound + 1) // cpus

class BoundsTransformer(ast.NodeTransformer):

    def __init__(self,loop):
        self.loop = loop
        self.top_level = False
        

    def visit_For(self, node):
        if not self.top_level:
            self.top_level = True
            self.generic_visit(node)
        self.top_level = False
        return node
        
    
    def visit_Call(self, node):
        if node.func.id == "range":
            # this needs to be changed at some point
            node.args[0] = ast.Num(n=slice_size(self.loop))
            return node
        else:
            self.generic_visit(node)
            
            
class AccessTransformer(ast.NodeTransformer):
    def __init__(self, loop):
        self.loop = loop
        self.in_access = False
        self.in_for = False
        self.slice_size = slice_size(loop)

    def visit_Subscript(self, node):
        top = False
        if not self.in_access:
            self.in_access = True
            top = True
        self.generic_visit(node)
        if top:
            self.in_access = False

    def visit_For(self, node):
        self.in_for = True
        self.generic_visit(node)
        

    # def visit_Name(self, node):
    #     if not self.in_access and not self.in_for:
    #         # if node.id == self.loop.target:
    #         #     return ast.parse("%s + proc_id * %d" % (node.id, self.slice_size)).body[0]
    #         pass
    #     else:
    #         if self.in_for:
    #             self.in_for = False
    #         self.generic_visit(node)


def generate_parallel_function(loop):
    # need to generate random string here
    name = "nest_fn" + str(id(loop))
    args = []
    for arg in loop.non_locals:
        args.append(ast.arg(arg=arg, annotation=None))
    args.append(ast.arg(arg="proc_id", annotation=None))
    args = ast.arguments(args=args, vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults = [])
#    return_values = (ast.parse(str(loop.non_locals))).body[0]
    return_values = [ast.Name(id=arg, ctx=ast.Load(), lineno=1, col_offset=0) for arg in loop.non_locals]
    print(return_values)
    return_stmt = ast.fix_missing_locations(ast.Return(value=return_values, lineno=1, col_offset=0))
    return_template = "return ["
    for i,arg in enumerate(loop.non_locals):
        if i ==0:
            return_template += "%s" % arg
        else:
            return_template += " ,%s" % arg
    return_template += "]"
    print("return values")
    print(return_stmt)
    transformed_tree = BoundsTransformer(loop).visit(loop.node)
#    transformed_tree = AccessTransformer(loop).visit(transformed_tree)
    # transformed_tree.lineno=0
    # transformed_tree.col_offset=0
    body = [transformed_tree, ast.parse(return_template).body[0]]
    dectorator_list = []
    fun_def = ast.FunctionDef(name=name, args=args, body=body, decorator_list=[], returns=None)
    return ast.fix_missing_locations(fun_def)


def generate_function_call(node_id, arr_args, index):
   # parsed_call = ast.parse("pool.apply_async(nest_fn%d)" % node_id)
    call = ast.Call()
    call.func = ast.Attribute(value=ast.Name(id='pool', ctx=ast.Load()), attr="apply_async", ctx=ast.Load())
    call.func.id = "nest_fn" + str(node_id) 
    call.func.ctx = ast.Load()
    print("printing arr_args")
    print(arr_args)
    # parsed_args = ast.parse(str(arr_args))
    parsed_args = [ast.parse(arg).body[0].value for arg in arr_args]
    parsed_args.append(ast.Num(n = index))
    fn_args= ast.List(elts=parsed_args, ctx=ast.Load())
    print("printing parsedarggs")
    print(parsed_args[0].lineno)
    call.args = [ast.Name(id="nest_fn%i" % node_id, ctx=ast.Load()),fn_args]
    call.keywords = []
    call.starargs = None
    call.kwargs = None
    return call
        

        
        

    


