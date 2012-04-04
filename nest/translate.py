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
        transformer = self.Transformer(parsed_code, safe_loops)
        transformed_tree = transformer.transform_tree()
        print(type(transformed_tree))
        transformed_tree = ast.fix_missing_locations(transformed_tree)
        for node in transformed_tree.body:
            ast.fix_missing_locations(node)
        print(ast.dump(transformed_tree))
        for node in ast.walk(transformed_tree):
            if isinstance(node, ast.expr) or isinstance(node, ast.stmt):
                node.lineno = 1
                if not node.lineno:
                    print(node.lineno)
                    print(node)
        
        output_code = compile(transformed_tree, self.filename, 'exec')
        #exec(output_code)

        

        

