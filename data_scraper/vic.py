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
            self.addEmail(row['Email'], member)
            self.addLink(row['WWW'], member)
            if row['PO Address line 1']:
                if row['PO Address line 3']:
                    addr_pcode = row['PO Address line 3'].split(' ')
                    line2 = row['PO Address line 2']
                else:
                    addr_pcode = row['PO Address line 2'].split(' ')
                    line2 = None
                self.addAddress(
                    models.AddressType.query.get(2),
                    row['PO Address line 1'],
                    line2,
                    addr_pcode[0],
                    None,
                    addr_pcode[1],
                    member
                )
            if row['Electorate Office Address line 1']:
                self.addAddress(
                    models.AddressType.query.get(1),
                    row['Electorate Office Address line 1'],
                    row['Electorate Office Address line 2'],
                    row['Electorate Office Address line 3'],
                    row['Electorate Office Address line 4'],
                    row['Electoral Office Postcode'],
                    member
                )
            if row['Ministerial Address line 1']:
                addr_pcode = row['PO Address line 3'].split(' ')
                self.addAddress(
                    models.AddressType.query.get(4),
                    row['Ministerial Address line 1'],
                    row['Ministerial Address line 2'],
                    row['Ministerial Address line 3'],
                    row['Ministerial Address line 4'],
                    row['Ministerial Postcode'],
                    member
                )
            self.addPhoneNumber(row['Phone'], 'electoral', member)
            self.addPhoneNumber(row['Ministerial Phone'], 'ministerial',
                                member)
            self.addPhoneNumber(row['Fax'], 'electoral fax', member)

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

    def addEmail(self, email, member):
        email = models.Email(email, member)
        db.session.add(email)

    def addLink(self, link, member):
        links = link.split(', ')
        if len(links) < 1:
            return None
        for link in links:
            link_type = 'website'
            if 'twitter' in link:
                link_type = 'twitter'
            if 'facebook' in link:
                link_type = 'facebook'
        db.session.add(models.Link(link, link_type, member))

    def addAddress(self, address_type, line1, line2, line3, line4, pcode,
                   member):
        if line1 is None:
            return
        state = 'Vic'
        address1 = line1
        address2 = None
        if line4 == 'VIC':
            address2 = line2
            suburb = line3
        else:
            suburb = line2
        address = models.Address(address1, address2, None, suburb,
                                 state, pcode, address_type, member, 0)
        db.session.add(address)

    def addPhoneNumber(self, number, type, member):
        if not number:
            return None
        phone = models.PhoneNumber(number, type, member)
        db.session.add(phone)
