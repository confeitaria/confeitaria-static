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
import requests

from inelegant.fs import temp_file, temp_dir
from inelegant.finder import TestFinder

from confeitaria.static.page import StaticPage
from confeitaria.server import Server

from confeitaria.static.store.file import FileStore


class TestStaticPage(unittest.TestCase):

    def test_serve_static_page(self):
        """
        This tests ensure that ``StaticPage`` serves the content of a file if
        it is found in its directory.
        """
        with temp_dir() as d, \
                temp_file(where=d, name='index.html', content='example') as f:

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/index.html')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)

    def test_serve_index_html(self):
        """
        This tests ensure that ``StaticPage`` will serve the content of
        ``index.html`` if requested to serve a directory.
        """
        with temp_dir() as d, \
                temp_file(where=d, name='index.html', content='example') as f:

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)

                r = requests.get('http://localhost:8000')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)

    def test_serve_subdir(self):
        """
        This tests ensure that ``StaticPage`` will serve the content of files
        from a subdirectory of the served dir.
        """
        with temp_dir() as d, \
                temp_dir(where=d, name='a/b/c') as sd, \
                temp_file(where=sd, name='index.html', content='example') as f:

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/a/b/c/index.html')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)

                r = requests.get('http://localhost:8000/a/b/c/')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)

    def test_serve_serve_404(self):
        """
        This tests ensure that ``StaticPage`` will return 404 if a file could
        not be found.
        """
        with temp_dir() as d, \
                temp_file(where=d, name='index.html', content='example') as f:

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/nofile.html')

                self.assertEquals(404, r.status_code)

    def test_serve_serve_404_subdir(self):
        """
        This tests ensure that ``StaticPage`` will return 404 if a file could
        not be found in a subdirectory.
        """
        with temp_dir() as d, \
                temp_dir(where=d, name='a/b/c') as sd, \
                temp_file(where=sd, name='index.html', content='example') as f:

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/a/b/c/nofile.html')

                self.assertEquals(404, r.status_code)

    def test_serve_serve_404_parent_dir(self):
        """
        This tests ensure that ``StaticPage`` will return 404 if a path tries
        to access a parent directory.
        """
        with temp_dir() as root_dir, \
                temp_dir(where=root_dir) as d, \
                temp_file(where=root_dir, name='passwd', content='example'):

            page = StaticPage(directory=d)

            with Server(page):
                r = requests.get('http://localhost:8000/../passwd')

                self.assertEquals(404, r.status_code)
                self.assertNotEquals('example', r.text)

    def test_page_can_use_store(self):
        """
        This tests ensure that ``StaticPage`` can receive a store instead of
        a directory directly.
        """
        with temp_dir() as d, \
                temp_file(where=d, name='index.html', content='example') as f:

            store = FileStore(directory=d)
            page = StaticPage(store=store)

            with Server(page):
                r = requests.get('http://localhost:8000/index.html')

                self.assertEquals(200, r.status_code)
                self.assertEquals('example', r.text)

    def test_page_has_default_index_html(self):
        """
        If we request the ``StaticPage`` root directory (e.g.
        ``http://localhost:8000``) it should provide a document with a basic
        introduction to the object itself.
        """
        with temp_dir() as d:
            store = FileStore(directory=d)
            page = StaticPage(store=store)

            with Server(page):
                r = requests.get('http://localhost:8000/index.html')

                self.assertEquals(200, r.status_code)
                self.assertTrue(r.text)


load_tests = TestFinder(
    __name__,
    'confeitaria.static.page'
).load_tests

if __name__ == '__main__':
    unittest.main()
