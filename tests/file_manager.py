#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseTestCase
from mock import Mock, patch
from data_scraper.file_manager import FileManager
import requests


class FileManagerTestCase(BaseTestCase):
    def setUp(self):
        self.file_manager = FileManager()

    def test_file_manager_response(self):
        file_content = 'some sort fo string'
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.content = file_content
            mock_response.status_code = 200
            self.assertEquals(
                file_content, self.file_manager.getPage('http://httpbin.org/'))

    def test_file_manager_exception(self):
        file_content = 'some sort fo string'
        with self.assertRaises(Exception):
            with patch.object(requests, 'get') as get_mock:
                get_mock.return_value = mock_response = Mock()
                mock_response.content = file_content
                mock_response.status_code = 500
                self.file_manager.getPage('http://httpbin/')

    def test_dict_reader(self):
        response_dict = """'first_name','second_name'
'Hammy','Goonan'"""
        response = self.file_manager.dictReader(response_dict)
        self.assertTrue(iter(response))
        self.assertIsInstance(next(response), dict)
