#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseData
from io import StringIO
from bs4 import BeautifulSoup
from yvih import models, db
import requests
import csv
import re


class VicData(BaseData):
    """Website is so bad that we're going to have to come back to this one and
    copy and paste data from a PDF into a csv file. No point doing it until the
    very last minute.
    """
    def vicData(self):
        data = self.getData()
        page = self.getPage()
        self.processData(data, page)

    def getData(self):
        """ Returns dictionary of CSV Data """
        url = 'http://www.parliament.vic.gov.au/members/house/mlc?format=csv'
        csvfile = requests.get(url, stream=True)
        return csv.DictReader(StringIO(csvfile.text))

    def getPage(self):
        url1 = 'http://www.parliament.vic.gov.au/members/house/mlc'
        url2 = ('http://www.parliament.vic.gov.au/members/results?houseabb='
                'mlc&page=2')
        page1 = requests.get(url1).content
        page2 = requests.get(url2).content
        return {'page_1': BeautifulSoup(page1), 'page_2': BeautifulSoup(page2)}

    def processData(self, data, page):
        for row in data:
            name = self.getName(row['Name'], page)
            electorate = self.getElectorate(row['Electorate'], 12)
            role = row['Ministry']
            party = self.getParty(row['Party'])
            photo = self.getPhoto(name, page)
            member = models.Member(name['first_name'], name['second_name'],
                                    role, electorate, party, photo)
            db.session.add(member)
            db.session.commit()

    def getName(self, name, page):
        titles = ['Ms', 'Mrs', 'Mr', 'Hon', 'Dr',
                  '(President', 'of', 'the', 'Legislative', 'Council)']
        name = name.split(' ')
        name_on_page = page['page_1'].find('a', text=re.compile(name[-1]))
        if not name_on_page:
            name_on_page = page['page_2'].find('a',
                                               text=re.compile(name[-1]))
        names = name_on_page.text.strip().split(' ')
        names = [n for n in names if n not in titles]
        return {'first_name': names[0], 'second_name': names[-1]}

    def getPhoto(self, name, page):
        link = page['page_1'].find('a', text=re.compile(name['second_name']))
        if not link:
            link = page['page_2'].find('a',
                                       text=re.compile(name['second_name']))
        url = 'http://www.parliament.vic.gov.au/' + link['href']
        member_page = requests.get(url).content
        member_page = BeautifulSoup(member_page)
        img = member_page.find('img', {"class": "details-portrait"})
        filename = '{}_{}.jpg'.format(name['first_name'], name['second_name'])
        return self.saveImg(img['src'], filename, 'vic')
