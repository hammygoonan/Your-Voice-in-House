import os
import json
import unittest
from yvih import app
from flask import Flask
from flask.ext.testing import TestCase
import tempfile

class YvihTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        self.maxDiff = None
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_home_displays_api(self):
        response = self.client.get('/')
        self.assertIn('Your Voice in House API', response.data)

    def test_non_get_method(self):
        response = self.client.post('/')
        self.assert405(response)

    def test_member_html(self):
        response = self.client.get('/members/')
        self.assertIn('Members', response.data)

    def test_member_json(self):
        headers = [('Accept', 'application/json')]
        response = self.client.get('/members/', headers=headers)
        self.assertIsInstance(response.json, dict)
        self.assertIn('members', response.json)

    def test_member_fields(self):
        response = self.client.get('/members/id/1')
        self.assert200(response)
        response = self.client.get('/members/first_name/Kate')
        self.assert200(response)
        response = self.client.get('/members/second_name/Smith')
        self.assert200(response)
        response = self.client.get('/members/first_name/Smith')
        self.assert404(response)
        response = self.client.get('/members/id/999999')
        self.assert404(response)
        response = self.client.get('/members/test/thing')
        self.assert404(response)
        # multiple parameters
        # id not an int
        pass
    def test_member_fields_json(self):
        headers = [('Accept', 'application/json')]
        response = self.client.get('/members/id/999999', headers=headers)
        self.assert404(response)
        response = self.client.get('/members/test/thing', headers=headers)
        self.assert404(response)




    # member id non-numeric returns 404
    # member id non-numeric json
    # 404 if no results

    # member first_name
    # member second_name
    # member role




if __name__ == '__main__':
    unittest.main()
