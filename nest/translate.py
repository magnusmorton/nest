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
    

    def __init__(self,filename=None, get_safe_loops_fn=None, transformer_fn=None):
        self.get_safe_loops_fn = get_safe_loops_fn
        self.transformer_fn = transformer_fn
        self.filename = filename

    def translate(self, source):
        parsed_code = ast.parse(source)
        safe_loops = self.get_safe_loops_fn(parsed_code)
        transformed_tree = self.transformer_fn(safe_loops)
        output_code = compile(transformed_tree, self.filename, 'exec')

        

        

