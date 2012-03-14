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

import unittest
from mock import *
from nest.translate import *

class TestTranslator(unittest.TestCase):
    """ I wish Python had something rspeccy"""
    
    @patch('builtins.compile')
    @patch('ast.parse')
    def setUp(self, mock_parse, mock_compile):
        """sets up fixtures...
        This is a bit of a mess"""
        self.mock_parse = mock_parse
        self.mock_parse.return_value = "FOO_PARSE"
        self.mock_get_safe_loops = Mock()
        self.loops = "LOOPS"
        self.mock_get_safe_loops.return_value = self.loops
        self.mock_transformer = Mock()
        self.mock_transformer.return_value = "CODE"
        self.mock_compile = mock_compile
        translator = Translator(filename='foo.py',get_safe_loops_fn=self.mock_get_safe_loops,
                transformer_fn=self.mock_transformer)
        translator.translate("foo")
    
    def test_translator_should_parse_input(self):
        self.mock_parse.assert_called_with("foo")
    
    def test_translator_should_analyse(self):
        self.mock_get_safe_loops.assert_called_with("FOO_PARSE")
    
    def test_translator_should_generate_code(self):
        self.mock_transformer.assert_called_with(self.loops)
    
    def test_translator_should_compile_code(self):
        self.mock_compile.assert_called_with("CODE","foo.py", 'exec')


        

