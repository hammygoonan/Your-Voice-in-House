#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import quote
from tests.base import BaseTestCase


class MembersTestCase(BaseTestCase):
    """ Member test case tests functionality of member pages. """
    def setUp(self):
        super().setUp()

    def test_member_html(self):
        response = self.client.get('/members/')
        self.assertIn('Members', response.data.decode('utf-8'))

    def test_member_json(self):
        headers = [('Accept', 'application/json')]
        response = self.client.get('/members/', headers=headers)
        self.assertIsInstance(response.json, dict)
        self.assertIn('members', response.json)

    def test_member_fields(self):
        response = self.client.get('/members/id/1')
        self.assert200(response)
        response = self.client.get('/members/id/non-numeric')
        self.assert400(response)
        response = self.client.get('/members/first_name/Hammy')
        self.assert200(response)
        response = self.client.get('/members/second_name/Goonan')
        self.assert200(response)
        response = self.client.get('/members/first_name/Abetz')
        self.assert404(response)
        response = self.client.get('/members/id/999999')
        self.assert404(response)
        response = self.client.get('/members/test/thing')
        self.assert400(response)
        response = self.client.get('/members/first_name/Hammy/role/internet')
        self.assert200(response)
        url = quote('/members/role/Minister for Internets')
        response = self.client.get(url)
        self.assert200(response)

    def test_member_fields_json(self):
        headers = [('Accept', 'application/json')]
        response = self.client.get('/members/id/1', headers=headers)
        self.assert200(response)
        response = self.client.get('/members/id/non-numeric', headers=headers)
        self.assert400(response)
        response = self.client.get('/members/first_name/Hammy',
                                   headers=headers)
        self.assert200(response)
        response = self.client.get(
            '/members/second_name/Goonan',
            headers=headers
        )
        self.assert200(response)
        response = self.client.get(
            '/members/first_name/Abetz',
            headers=headers
        )
        self.assert404(response)
        response = self.client.get('/members/id/999999', headers=headers)
        self.assert404(response)
        response = self.client.get('/members/test/thing', headers=headers)
        self.assert400(response)
        response = self.client.get(
            '/members/first_name/Hammy/role/internet',
            headers=headers
        )
        self.assert200(response)
        url = quote('/members/role/Minister for Internets')
        response = self.client.get(url)
        self.assert200(response)
        response = self.client.get('/members/id/1,2', headers=headers)
        self.assert200(response)
        self.assertTrue(len(response.json['members']) == 2)
