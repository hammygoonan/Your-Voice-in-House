#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import BaseTestCase

class HomeTestCase(BaseTestCase):
    def test_home_displays_api(self):
        response = self.client.get('/')
        self.assertIn('Your Voice in House', response.data.decode('utf-8'))
        self.assertIn('Search', response.data.decode('utf-8'))

    def test_non_get_method(self):
        response = self.client.post('/')
        self.assert405(response)
        headers = [('Accept', 'application/json')]
        response = self.client.post('/', headers=headers)
        self.assert405(response)
        self.assertIsInstance(response.json, dict)


if __name__ == '__main__':
    unittest.main()
