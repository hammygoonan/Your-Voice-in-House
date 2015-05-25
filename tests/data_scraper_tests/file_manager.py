#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseTestCase
from mock import Mock, patch
from data_scraper.file_manager import FileManager
from data_scraper.cache_manager import CacheManager
import requests
import shutil
import os


class FileManagerTestCase(BaseTestCase):
    def setUp(self):
        self.file_manager = FileManager()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        if os.path.isdir('../data_scraper/cache/'):
            shutil.rmtree('../data_scraper/cache/')

    @patch.object(CacheManager, 'checkCache')
    @patch.object(CacheManager, 'saveCache')
    def test_file_manager_response(self, save_cache_mock, check_cache_mock):
        file_content = 'some sort of string'
        check_cache_mock.return_value = None
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.content = file_content
            mock_response.status_code = 200
            self.assertEquals(
                file_content, self.file_manager.getPage('http://httpbin.org/'))

    @patch.object(CacheManager, 'checkCache')
    @patch.object(CacheManager, 'saveCache')
    def test_file_manager_exception(self, save_cache_mock, check_cache_mock):
        file_content = 'some sort fo string'
        check_cache_mock.return_value = None
        with self.assertRaises(Exception):
            with patch.object(requests, 'get') as get_mock:
                get_mock.return_value = mock_response = Mock()
                mock_response.content = file_content
                mock_response.status_code = 500
                self.file_manager.getPage('http://httpbin/')

    @patch.object(CacheManager, 'checkCache')
    @patch.object(CacheManager, 'saveCache')
    def test_dict_reader(self, save_cache_mock, check_cache_mock):
        check_cache_mock.return_value = None
        response_dict = """'first_name','second_name'
'Hammy','Goonan'"""
        response = self.file_manager.dictReader(response_dict)
        self.assertTrue(iter(response))
        self.assertIsInstance(next(response), dict)
