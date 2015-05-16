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
        houses = ['mlc', 'mla']
        for house in houses:
            data = self.getData(house)
            pages = self.getPages(
                'http://www.parliament.vic.gov.au/members/house/' + house
            )
            self.processData(data, pages, house)

    def getData(self, house):
        """ Returns dictionary of CSV Data """
        # 'http://www.parliament.vic.gov.au/members/house/mla?format=csv'
        csvfile = requests.get('http://www.parliament.vic.gov.au/' +
                               'members/house/' + house +
                               '?format=csv', stream=True)
        return csv.DictReader(StringIO(csvfile.text))

    def getPage(self, url):
        """ Returns BeautifulSoup object from url
        """
        page = requests.get(url).content
        soup = BeautifulSoup(page, "html5lib")
        return soup.find(id='member-list')

    def getPages(self, url):
        """ Get page from url. Finds next page and gets it until there are no
        more pages to get
        """
        pages = []
        next_page = True
        while next_page:
            page = self.getPage(url)
            pages.append(page)
            next_page = page.find('a', title="Next Page")
            if next_page:
                url = 'http://www.parliament.vic.gov.au/' + next_page['href']
        return pages

    def processData(self, data, pages, house):
        for row in data:
            name = self.getName(row['Name'], pages)
            house_id = 12 if house == 'mlc' else 13
            electorate = self.getElectorate(row['Electorate'], house_id)
            role = row['Ministry']
            party = self.getParty(row['Party'])
            photo = self.getPhoto(name, pages)
            member = models.Member(name['first_name'], name['second_name'],
                                   role, electorate, party, photo)
            db.session.add(member)
            self.addEmail(row['Email'], member)
            self.addLink(row['WWW'], member)
            if row['PO Address line 1']:
                if row['PO Address line 3']:
                    addr_pcode = row['PO Address line 3'].split(' ')
                    line2 = row['PO Address line 2']
                    if len(addr_pcode) == 1:
                        addr_pcode.append(None)
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

    def getName(self, name, pages):
        """ gets first name by searching member pages for surname match
        """
        titles = ['Ms', 'Mrs', 'Mr', 'Hon', 'Dr',
                  '(President', 'of', 'the', 'Legislative', 'Council)',
                  '(Premier)', '(Leader', 'of', 'the', 'Opposition)',
                  '(Speaker', 'of', 'the', 'Legislative', 'Assembly)',
                  '(Deputy', 'Premier)', '(Deputy', 'Leader', 'of', 'the',
                  'Opposition)']
        name = name.split(' ')
        # a pretty uncreative way of dealing with two members with the same
        # last name
        if name[-1] == 'Bull':
            if name[1] == 'Timothy':
                return {'first_name': 'Tim', 'second_name': 'Bull'}
            else:
                return {'first_name': 'Josh', 'second_name': 'Bull'}
        if name[-1] == 'O\'Brien':
            if name[1] == 'Michael':
                return {'first_name': 'Michael', 'second_name': 'O\'Brien'}
            else:
                return {'first_name': 'Danny', 'second_name': 'O\'Brien'}
        if name[-1] == 'Richardson':
            if name[1] == 'Fiona':
                return {'first_name': 'Fiona', 'second_name': 'Richardson'}
            else:
                return {'first_name': 'Tim', 'second_name': 'Richardson'}
        if name[-1] == 'Smith':
            if name[1] == 'Ryan':
                return {'first_name': 'Ryan', 'second_name': 'Smith'}
            else:
                return {'first_name': 'Tim', 'second_name': 'Smith'}
        for page in pages:
            name_on_page = page.find(
                'a', text=re.compile(' {}'.format(name[-1]))
            )
            if name_on_page:
                break
        names = name_on_page.text.strip().split(' ')
        names = [n for n in names if n not in titles]
        return {'first_name': names[0], 'second_name': names[-1]}

    def getPhoto(self, name, pages):
        for page in pages:
            member_name = '{} {}'.format(
                name['first_name'], name['second_name']
            )
            link = page.find('a', text=re.compile(member_name))
            if link:
                break
        url = 'http://www.parliament.vic.gov.au/' + link['href']
        member_page = requests.get(url).content
        member_page = BeautifulSoup(member_page)
        img = member_page.find('img', {"class": "details-portrait"})
        filename = '{}.jpg'.format(member_name)
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
