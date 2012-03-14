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
    
    @patch('ast.parse')
    def setUp(self, mock_parse):
        """sets up fixtures"""
        self.mock_parse = mock_parse
        self.mock_parse.return_value = "FOO_PARSE"
        self.mock_get_safe_loops = Mock()
        self.mock_get_safe_loops.return_value = []
        translator = Translator(get_safe_loops_fn=self.mock_get_safe_loops)
        translator.translate("foo")
    
    def test_translator_should_parse_input(self):
        self.mock_parse.assert_called_with("foo")
    
    #@unittest.skip("need to add some stuff to the loop module")
    def test_translator_should_analyse(self):
        self.mock_get_safe_loops.assert_called_with("FOO_PARSE")
        

