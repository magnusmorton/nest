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
import pdb
import sys
import marshal
import imp
import unparse
class Translator(object):
    

    def __init__(self,filename=None, get_safe_loops_fn=None, Transformer_class=None):
        self.get_safe_loops_fn = get_safe_loops_fn
        self.Transformer = Transformer_class
        self.filename = filename

    def translate(self, source):
        parsed_code = ast.parse(source)
        safe_loops = self.get_safe_loops_fn(parsed_code)
        if not safe_loops:
            print("No safe loops found")
        print(safe_loops)
        print(safe_loops[0].all_statements)
        print(ast.dump(parsed_code))
        transformer = self.Transformer(ast.increment_lineno(parsed_code, 100), safe_loops)
        transformed_tree = transformer.transform_tree()
#        transformed_tree.lineno =1 
 #       transformed_tree.col_offset = 0        
        print(type(transformed_tree))
        transformed_tree = ast.fix_missing_locations(transformed_tree)
        
        # print(ast.dump(transformed_tree))
        # for node in ast.walk(transformed_tree):
        #     if isinstance(node, ast.expr) or isinstance(node, ast.stmt):
        #         print(node.lineno)
        #         print(node)
        
        unparse.Unparser(transformed_tree, sys.stdout)
        output_code = compile(transformed_tree, self.filename, 'exec')
        pmod = ParallelModule()
        try:
            with open('output.py','w') as f:
                unparse.Unparser(transformed_tree, f)
        #    f.write(imp.get_magic())
         #   marshal.dump(output_code, f)
        #    exec(output_code,{})
            
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(sys.exc_info()[2])
        

        

class ParallelModule(object):
    pass
        

