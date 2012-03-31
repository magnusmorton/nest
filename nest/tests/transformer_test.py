import unittest
import mock
from nest.transformer import *


class TransformerTests(unittest.TestCase):
    
    def test_generate_slices_simple(self):
        loop = mock.Mock()
        loop.upper_bound = 1000
        loop.lower_bound = 0
        expected = [(0, 500), (500, 1000)]
        self.assertEqual(expected, generate_slices(loop, 2)) 
