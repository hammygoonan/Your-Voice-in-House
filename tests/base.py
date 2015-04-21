#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
from yvih import app, db

class BaseTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        self.maxDiff = None
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
