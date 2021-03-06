#!/usr/bin/env python
#
# Copyright 2015 Adam Victor Brandizzi
#
# This file is part of Confeitaria Static.
#
# Confeitaria Static is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Confeitaria Static is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Confeitaria Static.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from inelegant.finder import TestFinder

load_tests = TestFinder(
    'confeitaria_static_tests.page',
    'confeitaria_static_tests.store.aggregate',
    'confeitaria_static_tests.store.fake',
    'confeitaria_static_tests.store.file',
    'confeitaria_static_tests.store.resource'
).load_tests

if __name__ == "__main__":
    unittest.main()
