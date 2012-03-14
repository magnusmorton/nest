#!/usr/bin/env python
# encoding: utf-8
"""
nest.py

Created by Magnus Morton on 2012-03-14.
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

"""

import sys
import os
import argparse
import nest.translate
import ast
from nest.loop import get_safe_loops


def main():
    parser = argparse.ArgumentParser(description='implicitly parallelising Python')
    parser.add_argument('file')
    args = parser.parse_args()
    source_file = args.file
    translator = nest.translate.Translator(source_file, get_safe_loops, transformer_fn)
    with open(source_file, 'r') as the_file:
        translator.translate(the_file.read())

if __name__ == '__main__':
	main()


def transformer_fn(dummy):
    return ast.parse("print('this is a dummy run')")