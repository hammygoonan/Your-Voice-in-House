#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yvih import db
from yvih.models import DataCache
import hashlib
import datetime
import os


class CacheManager(object):
    """ manages the caching of requests """
    def __init__(self):
        self.age = {'days': 5}
        self.content = None

    def checkCache(self, url):
        """ checks to see is a recently cached version of the file exists """
        cache = DataCache.query.filter_by(url=url).first()
        # if nothing cached
        if not cache:
            return None
        # check age of cache and return if under specified age
        with open(cache.local_storage, 'r') as file:
            if(
                cache.date > datetime.datetime.now()
                - datetime.timedelta(**self.age)
            ):
                self.content = file.read()
                return self.content
        return None

    def saveCache(self, url, content):
        """ saves cached files. """
        md5 = hashlib.md5(content.encode('utf-8')).hexdigest()
        date_time = datetime.datetime.now()
        local_storage = 'data_scraper/cache/{}.txt'.format(md5)
        if not os.path.isdir('data_scraper/cache'):
            os.makedirs('data_scraper/cache')
        with open(local_storage, 'wb') as cached_response:
            cached_response.write(bytes(content, 'UTF-8'))
        db.session.add(DataCache(date_time, url, md5, local_storage))
        db.session.commit()
