#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_scraper.base import BaseData
from tests.base import BaseTestCase


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
