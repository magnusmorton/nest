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
    def setUp(self):
        """sets up fixtures"""
        pass
    
    @patch('ast.parse')
    def test_translator_should_parse_input(self, mock_parse):
        translator = Translator()
        translator.translate("foo")
        mock_parse.assert_called_with("foo")

