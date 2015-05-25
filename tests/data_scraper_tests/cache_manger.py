#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import BaseTestCase
from data_scraper.cache_manager import CacheManager
import shutil
import os
# from mock import Mock, patch
# from data_scraper.file_manager import FileManager
# import requests


class FileManagerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cache_manager = CacheManager()
        self.cache_content = 'this is test content'
        self.cache_path = os.path.realpath('data_scraper/cache')
        if not os.path.isdir(self.cache_path):
            os.mkdir(self.cache_path)
        file_path = self.cache_path + '/b0da4eeb66a12a9ba07cb2f86a967129.txt'
        file = open(file_path, 'w')
        file.write(self.cache_content)
        file.close()

    def tearDown(self):
        if os.path.isdir(self.cache_path):
            shutil.rmtree(self.cache_path)
        super().tearDown()

    def test_check_cache(self):
        self.assertEquals(None,
                          self.cache_manager.checkCache('http://test.com'))

        # returns old file
        # returns new file if old file is old

        self.assertIsInstance(
            self.cache_manager.checkCache('http://httpbin.org'),
            str
        )

    def test_cache_save(self):
        # creates new file
        # creates new entry in db
        pass
