#!/usr/bin/env python
# -*- coding: utf-8 -*-

from data_scraper.base import BaseData
from tests.base import BaseTestCase
from yvih import models
import re


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
        address_type = models.AddressType.query.get(1)
        address = {'line1': 'PO Box 42', 'suburb': 'Melbourne', 'pcode': 3000,
                   'state': 'Vic', 'member': member,
                   'address_type': address_type}
        self.assertTrue(
            isinstance(self.base_data.getAddress(**address), models.Address)
        )
        address['address_type'] = 2
        self.assertTrue(
            isinstance(self.base_data.getAddress(**address), models.Address)
        )
        address['address_type'] = 'Postal'
        with self.assertRaises(TypeError):
            self.base_data.getAddress(**address)
        address['member'] = 2
        address['address_type'] = 4
        with self.assertRaises(TypeError):
            self.base_data.getAddress(**address)

    def test_get_link(self):
        member = models.Member.query.get(1)
        link = 'http://httpbin.org/'
        link_type = 'twitter'
        self.assertTrue(
            isinstance(self.base_data.getLink(link, link_type, member),
                       models.Link)
        )
        with self.assertRaises(ValueError):
            self.base_data.getLink(link, 'wrong type', member)
        with self.assertRaises(ValueError):
            self.base_data.getLink('bin.org', link_type, member)
        with self.assertRaises(TypeError):
            self.base_data.getLink(link, link_type, 'member')

    def test_get_email(self):
        member = models.Member.query.get(1)
        email = 'test@test.org'
        self.assertTrue(
            isinstance(self.base_data.getEmail(email, member), models.Email)
        )
        with self.assertRaises(ValueError):
            self.base_data.getEmail('not an email', member)
        with self.assertRaises(TypeError):
            self.base_data.getEmail(email, 'not an member')

    def test_get_phone_number(self):
        number = '03 9876 2384'
        number_type = 'electoral fax'
        member = models.Member.query.get(1)
        self.assertTrue(
            isinstance(
                self.base_data.getPhoneNumber(number, number_type, member),
                models.PhoneNumber
            )
        )
        with self.assertRaises(ValueError):
            self.base_data.getPhoneNumber(98765, number_type, member)
        with self.assertRaises(ValueError):
            self.base_data.getPhoneNumber(number, 'test', member)
        with self.assertRaises(TypeError):
            self.base_data.getPhoneNumber(number, number_type, 'test')

    def test_get_party(self):
        party = "Australian Greens"
        self.assertTrue(
            isinstance(self.base_data.getParty(party),  models.Party)
        )
        with self.assertRaises(ValueError):
            self.base_data.getParty('Mad Hatters')

    def test_get_electorate(self):
        chamber = models.Chamber.query.get(2)
        self.assertTrue(
            isinstance(self.base_data.getElectorate('Test Electorate', 1),
                       models.Electorate)
        )
        self.assertTrue(
            isinstance(self.base_data.getElectorate('New Electorate', 1),
                       models.Electorate)
        )
        self.assertTrue(
            isinstance(self.base_data.getElectorate('Test Electorate',
                                                    chamber),
                       models.Electorate)
        )
        self.assertTrue(
            isinstance(self.base_data.getElectorate('New Electorate', chamber),
                       models.Electorate)
        )
        with self.assertRaises(ValueError):
            self.base_data.getElectorate('New Electorate', 99)
        with self.assertRaises(ValueError):
            self.base_data.getElectorate('New Electorate', 'test')


    def test_get_photo(self):
        pass
