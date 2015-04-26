#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from .base import BaseData
from bs4 import BeautifulSoup


class ActData(BaseData):
    def __init__(self):
        super(ActData, self).__init__()
        self.list_url = 'http://www.parliament.act.gov.au/members/current'

    def actData(self):
        page = requests.get(self.list_url).content
        soup = BeautifulSoup(page)
