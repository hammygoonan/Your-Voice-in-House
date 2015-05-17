#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseData
from bs4 import BeautifulSoup
import requests
import os
import re
import xlrd
from yvih import models, db


class WaData(BaseData):
    """Scraper for Western Australian Parliament.
    """
    def __init__(self):
        self.houses = {
            'council': {
                'csv': 'http://www.parliament.wa.gov.au/WebCMS/WebCMS.nsf/re' +
                       'sources/file-data-for-legislative-council-members/$f' +
                       'ile/DATA%20FOR%20LEGISLATIVE%20COUNCIL%20MEMBERS%201' +
                       '1032015.xls',
                'site': 'http://www.parliament.wa.gov.au/parliament/memblist' +
                        '.nsf/WCouncilMembers?openform'
            },
            'assembly': {
                'csv': 'http://www.parliament.wa.gov.au/WebCMS/WebCMS.nsf/re' +
                       'sources/file-mla-merge-data/$file/MLA%20Merge%20Data' +
                       '%2020150205.xls',
                'site': 'http://www.parliament.wa.gov.au/parliament/memblist' +
                        '.nsf/WAssemblyMembers?openform'
            }
        }

    def waData(self):
        for house, urls in self.houses.items():
            data = self.getData(urls['csv'])
            if house == 'council':
                self.getCouncilMembers(data)
            else:
                self.getAssemblyMembers(data)

    def getCouncilMembers(self, data):
        page = self.getPage(self.houses['council']['site'])
        for row in data:
            member_page = self.getMemberPage(page, row[2])
            party = self.getParty(row[10])
            electorate = self.getElectorate(row[11], 15)
            role = self.getRole(
                row[8], row[7]
            )
            fname = '{}_{}.jpg'.format(row[5], row[2])
            photo = self.getPhoto(member_page, fname)
            member = models.Member(row[5], row[2],
                                   role, electorate, party, photo)
            db.session.add(member)
            self.getLinks(page, member)
            if(row[12]):
                self.getAddress(row[12], 7, member)
            self.getAddress(row[13], 2, member)
            self.getAddress(row[14], 1, member)
            self.getAddress(row[15], 4, member)
            self.getPhone(member_page, member)

            db.session.commit()

    def getAssemblyMembers(self, data):
        page = self.getPage(self.houses['assembly']['site'])
        for row in data:
            member_page = self.getMemberPage(page, row[3])
            party = self.findParty(page, row[3])
            electorate = self.getElectorate(row[5].replace('Member for ', ''),
                                            14)
            role = row[6]
            fname = '{}_{}.jpg'.format(row[2], row[3])
            photo = self.getPhoto(member_page, fname)
            member = models.Member(row[2], row[3],
                                   role, electorate, party, photo)
            db.session.add(member)
            self.getLinks(page, member)
            if(row[8]):
                self.getAddress('{}\n{}'.format(row[8], row[9]), 6, member)
            self.getAddress('{}\n{}'.format(row[10], row[11]), 1, member)
            self.getAddress('{}\n{}'.format(row[12], row[13]), 2, member)
            self.getAddress('{}\n{}'.format(row[14], row[15]), 4, member)
            self.getPhone(member_page, member)

            db.session.commit()

    def getRole(self, ministerial, other):
        if ministerial and not other:
            return ministerial
        if other and ministerial:
            return '{}\n{}'.format(other, ministerial)
        if other and not ministerial:
            return other
        return None

    def getPhoto(self, member_page, filename):
        td = member_page.find('td', width=198)
        img = td.find('img')
        img = img['src'].replace('..', 'http://www.parliament.wa.gov.au/'
                                       'Parliament/Memblist.nsf/')
        return self.saveImg(img, filename, 'wa')

    def getLinks(self, page, member):
        member_link = page.find('b', text=re.compile(member.second_name))
        td = member_link.find_parent('tr')
        for link in td.find_all('a'):
            if('mailto:' in link['href'] and
               link['href'].replace('mailto:', '') != ''):
                db.session.add(
                    models.Email(link['href'].replace('mailto:', ''), member)
                )
            elif('http' in link['href'] and
                 link['href'].replace('http://', '') != ''):
                db.session.add(
                    models.Link(link['href'], 'website', member)
                )

    def getAddress(self, address, type_id, member):
        address_type = models.AddressType.query.get(type_id)
        address_lines = address.split('\n')
        addr1 = address_lines[0].strip()
        addr2 = None
        if len(address_lines) > 2:
            addr2 = address_lines[1].strip()
        pcode = re.search('[0-9]{4}', address_lines[-1].strip())
        pcode = pcode.group(0)
        suburb = address_lines[-1].replace(pcode, '').replace('WA', '').strip()
        db.session.add(models.Address(addr1, addr2, None, suburb, 'WA', pcode,
                                      address_type, member, 0))

    def getPhone(self, member_page, member):
        offices = [('Electorate Office:', 'electoral'),
                   ('Other Office:', 'alternative'),
                   ('Ministerial Office:', 'ministerial')]
        numbers = {
            'freecall': re.compile('Freecall:\ [0-9\ ]{12}'),
            'phone': re.compile('Ph:\ [0-9()]{0,4}[0-9\ ]{9,14}'),
            'fax': re.compile('Fax:\ [0-9()]{0,4}[0-9\ ]{9,14}')
        }

        for office in offices:
            office_text = member_page.find(text=re.compile(office[0]))
            if office_text:
                tr = office_text.find_parent('tr')
                address_block = tr.find_next_sibling('tr').text

                for no_type, regex in numbers.items():
                    number = regex.search(address_block)
                    if number:
                        # change phone to ph to then remove it from number
                        replace_pre = no_type.replace('phone', 'ph')\
                            .title() + ': '
                        no = number.group(0).replace(replace_pre, '')
                        no_type = office[1] + ' ' + no_type
                        phone = models.PhoneNumber(no, no_type, member)
                        db.session.add(phone)

    def findParty(self, page, second_name):
        name = page.find('b', text=re.compile(second_name))
        tr = name.find_parent('tr')
        regex = re.compile('Party: [A-Za-z]{3}')
        party = regex.search(tr.text)
        return self.getParty(party.group(0).replace('Party: ', ''))

    def getMemberPage(self, page, second_name):
        member = page.find('b', text=re.compile(second_name))
        member_page = self.getPage('http://www.parliament.wa.gov.au/' +
                                   member.parent['href'])
        return member_page

    def getData(self, url):
        """ Returns dictionary of CSV Data """
        csvfile = requests.get(url, stream=True)
        temp_file = 'temp.xls'
        with open(temp_file, 'wb') as f:
            for chunk in csvfile.iter_content():
                f.write(chunk)
        f.close()
        book = xlrd.open_workbook(temp_file)
        sheet_names = book.sheet_names()
        sheet = book.sheet_by_name(sheet_names[0])
        # header = sheet.row_values(0)
        values = []
        for rownum in range(1, sheet.nrows):
            values.append(
                # dict(zip(header, sheet.row_values(rownum)))
                sheet.row_values(rownum)
            )
        os.remove(temp_file)
        return values

    def getPage(self, url):
        """ Returns BeautifulSoup object from url """
        page = requests.get(url).content
        soup = BeautifulSoup(page, "html5lib")
        return soup
