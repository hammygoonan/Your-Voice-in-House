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

            address = models.Address(
                row['CONTACT ADDRESS LINE1'],
                row['CONTACT ADDRESS LINE2'],
                row['CONTACT ADDRESS LINE3'],
                row['CONTACT ADDRESS SUBURB'],
                row['CONTACT ADDRESS STATE'],
                row['CONTACT ADDRESS POSTCODE'],
                models.AddressType.query.get(2),
                member,
                0
            )
            db.session.add(address)
            if row['CONTACT ADDRESS POBOX '] != '':
                address = models.Address(
                    row['CONTACT ADDRESS POBOX '],
                    None,
                    None,
                    row['CONTACT ADDRESS POBOX SUBURB'],
                    row['CONTACT ADDRESS POBOX STATE'],
                    row['CONTACT ADDRESS POBOX POSTCODE'],
                    models.AddressType.query.get(1),
                    member,
                    0
                )
                db.session.add(address)
            if row['MINISTERIAL OFFICE ADDRESS LINE1'] != '':
                address = models.Address(
                    row['MINISTERIAL OFFICE ADDRESS LINE1'],
                    row['MINISTERIAL OFFICE ADDRESS LINE2'],
                    row['MINISTERIAL OFFICE ADDRESS LINE3'],
                    row['MINISTERIAL OFFICE ADDRESS SUBURB'],
                    row['MINISTERIAL OFFICE ADDRESS STATE'],
                    row['MINISTERIAL OFFICE ADDRESS POSTCODE'],
                    models.AddressType.query.get(7),
                    member,
                    0
                )
                db.session.add(address)
            if row['MINISTERIAL OFFICE POBOX '] != '':
                address = models.Address(
                    row['MINISTERIAL OFFICE POBOX '],
                    None,
                    None,
                    row['MINISTERIAL OFFICE POBOX SUBURB'],
                    row['MINISTERIAL OFFICE POBOX STATE'],
                    row['MINISTERIAL OFFICE POBOX POSTCODE'],
                    models.AddressType.query.get(6),
                    member,
                    0
                )
                db.session.add(address)
            if row['ALTERNATIVE OFFICE ADDRESS LINE1'] != '':
                address = models.Address(
                    row['ALTERNATIVE OFFICE ADDRESS LINE1'],
                    row['ALTERNATIVE OFFICE ADDRESS LINE2'],
                    row['ALTERNATIVE OFFICE ADDRESS LINE3'],
                    row['ALTERNATIVE OFFICE ADDRESS SUBURB'],
                    row['ALTERNATIVE OFFICE ADDRESS STATE'],
                    row['ALTERNATIVE OFFICE ADDRESS POSTCODE'],
                    models.AddressType.query.get(5),
                    member,
                    0
                )
                db.session.add(address)
            if row['ALTERNATIVE OFFICE POBOX '] != '':
                address = models.Address(
                    row['ALTERNATIVE OFFICE POBOX '],
                    None,
                    None,
                    row['ALTERNATIVE OFFICE POBOX SUBURB'],
                    row['ALTERNATIVE OFFICE POBOX STATE'],
                    row['ALTERNATIVE OFFICE POBOX POSTCODE'],
                    models.AddressType.query.get(5),
                    member,
                    0
                )
                db.session.add(address)

            # add emails
            email_types = [row['CONTACT ADDRESS EMAIL'],
                           row['MINISTERIAL OFFICE EMAIL'],
                           row['ALTERNATIVE OFFICE EMAIL']]
            for email in email_types:
                if email != '':
                    emails = models.Email(email, member)
                db.session.add(emails)

            numbers = [(row['CONTACT ADDRESS PHONE'], 'electoral'),
                       (row['CONTACT ADDRESS FAX'], 'electoral fax'),
                       (row['MINISTERIAL OFFICE PHONE'], 'ministerial phone'),
                       (row['MINISTERIAL OFFICE FAX'], 'ministerial fax'),
                       (row['ALTERNATIVE OFFICE PHONE'], 'alternative phone'),
                       (row['ALTERNATIVE OFFICE FAX'], 'alternative fax')]

            for number in numbers:
                if number[0] != '':
                    ph_number = models.PhoneNumber(number[0], number[1],
                                                   member)
                    db.session.add(ph_number)

            sites = [row['MINISTERIAL OFFICE WEBSITE'],
                     row['ALTERNATIVE OFFICE WEBSITE']]
            for site in sites:
                if site != '':
                    link = models.Link(site, 'website', member)
                    db.session.add(link)
            db.session.commit()

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
