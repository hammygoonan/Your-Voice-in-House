#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseData
import requests
import csv
import re
from io import StringIO
from bs4 import BeautifulSoup
from yvih import models, db


class NswData(BaseData):
    """A scrape of all NSW parliamentary data"""
    def __init__(self):
        self.csv = 'http://parliament.nsw.gov.au/prod/parlment/members.nsf/' +\
                   'reports/ContactSpreadsheetAll.csv'
        self.url = 'http://parliament.nsw.gov.au/prod/parlment/members.nsf/' +\
                   'V3ListCurrentMembers'

    def nswData(self):
        data = self.getData()
        page = self.getPage(self.url)
        for row in data:
            second_name = row['SURNAME']
            first_name = self.getFirstName(row['SURNAME'], page)
            party = self.getParty(row['PARTY'])
            if row['ELECTORATE'] == '':
                electorate = self.getElectorate('New South Wales', 5)
            else:
                electorate = self.getElectorate(row['ELECTORATE'], 4)
            role = self.getRole(row['OFFICE HOLDER'], row['MINISTRY'])
            photo = self.getPhoto(first_name, second_name, page)
            member = models.Member(first_name, second_name, role, electorate,
                                   party, photo)
            db.session.add(member)

    def getFirstName(self, second_name, page):
        """ gets member name from page. First name isn't provided in csv """
        name_text = page.find('a', text=re.compile(second_name))
        name = name_text.text.split(', ')
        return name[1]

    def getRole(self, office, ministry):
        if office == '' and ministry == '':
            return None
        if office == '':
            return ministry
        if ministry == '':
            return office
        return '{} \n {}'.format(ministry, office)

    def getPhoto(self, first_name, second_name, page):
        link = page.find('a', text=re.compile(second_name))
        member_page = self.getPage('http://parliament.nsw.gov.au/' +
                                   link['href'])
        body = member_page.find('div', {'class': 'bodyText'})
        header = body.find('h1')
        img = header.find_next_siblings('img')
        if img:
            filename = '{}_{}.jpg'.format(first_name, second_name)
            src = 'http://parliament.nsw.gov.au/' + img[0]['src']
            return self.saveImg(src, filename, 'nsw')
        return None

    def getData(self):
        """ Returns dictionary of CSV Data """
        csvfile = requests.get(self.csv, stream=True)
        return csv.DictReader(StringIO(csvfile.text))

    def getPage(self, url):
        """ Returns BeautifulSoup object from url """
        page = requests.get(url).content
        return BeautifulSoup(page, "html5lib")
