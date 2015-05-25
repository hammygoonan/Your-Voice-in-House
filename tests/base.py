#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from flask.ext.testing import TestCase
from yvih import app, db
from tests.create_db import create_test_db


class BaseTestCase(TestCase):
    """Base test class that all other test inherit. Sets up and tears down context.
    """
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        create_test_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
