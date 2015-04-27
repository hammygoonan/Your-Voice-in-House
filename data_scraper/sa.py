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
            role = self.getRole(page)
            party = self.getParty(page)
            electorate = self.getElectorate(page)
            print(role)
            print(party)
            print(electorate)

    def getMemberPage(self, url):
        page = requests.get(url).content
        return BeautifulSoup(page)

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
