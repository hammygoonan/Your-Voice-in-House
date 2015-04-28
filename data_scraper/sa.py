#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from .base import BaseData


class SaData(BaseData):
    """Scrape SA Parliament website for member data
    """
    def __init__(self):
        self.url = ('https://www2.parliament.sa.gov.au/Internet/DesktopModules'
                    '/Memberlist.aspx')

    def saData(self):
        page = requests.get(self.url).content
        soup = BeautifulSoup(page)
        for link in soup.find_all('a')[4:]:
            page = self.getMemberPage('https://www2.parliament.sa.gov.au/'
                                      'Internet/DesktopModules/'
                                      + link['href'])
            name = self.getName(page)
            role = self.getRole(page)
            party = self.getParty(page)
            electorate = self.getElectorate(page)
            photo = self.getPhoto(page, name)

    def getMemberPage(self, url):
        page = requests.get(url).content
        return BeautifulSoup(page)

    def getName(self, page):
        text = page.find('td', align='right').text.split()
        first_name = text[-2]
        second_name = text[-1]
        return {'first_name': first_name, 'second_name': second_name}

    def getRole(self, page):
        position = page.find('td', text=re.compile("Position"))
        position = position.next_sibling.text
        if position == 'member' or position == 'minister':
            position = None
        return position

    def getParty(self, page):
        party = page.find('td', text=re.compile("Political Party"))
        party = party.next_sibling.text
        return super(SaData, self).getParty(party)

    def getElectorate(self, page):
        house = page.find('td', text=re.compile("House"))
        house = house.next_sibling.text
        house = 8 if house == 'House of Assembly' else 9
        electorate = page.find('td', text=re.compile("Electorate"))
        electorate = electorate.next_sibling.text
        return super(SaData, self).getElectorate(electorate, house)

    def getPhoto(self, page, name):
        img = page.find_all('img')
        src = 'https://www2.parliament.sa.gov.au{}'.format(img[2]['src'])
        filename = '{}_{}.jpg'.format(name['first_name'], name['second_name'])
        return self.saveImg(src, filename, 'sa')
