#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_scraper.base import BaseData
from tests.base import BaseTestCase
from yvih import models


class BaseDataTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.base_data = BaseData()

    def test_get_name(self):
        self.assertTrue(
            isinstance(self.base_data.getName('Hammy', 'Goonan'), dict)
        )
        with self.assertRaises(ValueError):
            self.base_data.getName('Hammy Goonan')
        with self.assertRaises(ValueError):
            self.base_data.getName(['Hammy', 'The Boss', 'Goonan'])
        with self.assertRaises(ValueError):
            self.base_data.getName('Hammy', 'The Boss', 'Goonan')

    def test_get_role(self):
        self.assertTrue(
            isinstance(self.base_data.getRole('This is a role'), str)
        )
        with self.assertRaises(TypeError):
            self.base_data.getRole(1)
        # @ todo BeautifulSoup mocked response ?

    def test_get_address(self):
        member = models.Member.query.get(1)
        address_type = models.Member.query.get(1)
        address = {'line1': 'PO Box 42', 'suburb': 'Melbourne', 'pcode': 3000,
                   'state': 'Vic', 'member': member,
                   'address_type': address_type}
        self.assertTrue(
            isinstance(self.base_data.getAddress(**address), models.Address)
        )
        address['member'] = 2
        with self.assertRaises(TypeError):
            self.base_data.getAddress(**address)
