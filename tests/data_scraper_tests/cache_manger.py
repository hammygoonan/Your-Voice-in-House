#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import BaseTestCase
from data_scraper.cache_manager import CacheManager
from yvih.models import DataCache
import shutil
import os
import datetime


class FileManagerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cache_manager = CacheManager()
        self.cache_content = 'this is test content'
        self.cache_path = os.path.realpath('data_scraper/cache')
        self.md5 = 'b0da4eeb66a12a9ba07cb2f86a967129'
        if not os.path.isdir(self.cache_path):
            os.mkdir(self.cache_path)
        self.file_path = '{}/{}.txt'.format(self.cache_path, self.md5)
        file = open(self.file_path, 'w')
        file.write(self.cache_content)
        file.close()

    def tearDown(self):
        if os.path.isdir(self.cache_path):
            shutil.rmtree(self.cache_path)
        super().tearDown()

    def test_check_cache(self):
        # should return None if cache doesn't exist
        self.assertEquals(None,
                          self.cache_manager.checkCache('http://test.com'))
        # should return cache_content if cache does exist
        self.assertEquals(
            self.cache_content,
            self.cache_manager.checkCache('http://httpbin.org'),
        )
        # should return None if cache file is over 5 days ago
        time = datetime.datetime(2015, 1, 1)
        time = time.timestamp()
        os.utime(self.file_path, (time, time))
        self.assertEquals(None,
                          self.cache_manager.checkCache('http://test.com'))

    def test_cache_save(self):
        url = 'http://httpbin.org'
        self.cache_manager.saveCache(url, self.cache_content)
        self.assertTrue(os.path.isfile(self.file_path))
        with open(self.file_path, 'r') as file:
            self.assertEquals(self.cache_content, file.read())
        db_entry = DataCache.query.filter_by(url=url).first()
        self.assertIsInstance(db_entry, DataCache)
