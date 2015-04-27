#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from .base import BaseData
from bs4 import BeautifulSoup
from yvih.models import Member, Link, Email, Address, PhoneNumber, AddressType
from yvih import db
import base64


class ActData(BaseData):
    """Scrapes the ACT Parliament website for member details"""
    def __init__(self):
        self.list_url = 'http://www.parliament.act.gov.au/members/current'

    def actData(self):
        """Scrape ACT Current members page for member details"""
        page = requests.get(self.list_url).content
        soup = BeautifulSoup(page, "html5lib")
        table = soup.find('table', 'tablesorter')
        for tr in table.find_all('tr'):
            td = tr.find_all('td')
            if not td:
                # first and last rows are blank
                continue
            name = td[0].text.split(', ')
            first_name = name[1]
            second_name = name[0]
            role_contents = td[1].contents
            roles = []
            for x in role_contents:
                if x.string:
                    roles.append(x.string)
            role = "\n".join(roles)
            electorate = self.getElectorate(td[2].text.strip(), 3)
            party = self.getParty(td[3].text)
            photo = None
            member = Member(
                first_name, second_name, role, electorate, party, photo
            )
            db.session.add(member)
            member.photo = self.getPhoto(td[0], member)
            self.getAddress(member)
            self.getLinks(td[4], member)
            self.getPhone(td[4], member)
            db.session.commit()

    def getPhoto(self, link, member):
        """Return photo field for member.
        Takes BeautifulSoup td object with link, follows the link and gets the
        member photo which is then saved.
        """
        url = link.find('a')
        page = requests.get(url['href']).content
        soup = BeautifulSoup(page, "html5lib")
        section = soup.find('div', 'section')
        img = section.find('img')
        if img['src'].find('base64') > -1:
            base64_img = base64.b64decode(img['src'].split(',')[1])
            photo = 'act/{}_{}.jpg'.format(
                member.first_name, member.second_name
            )
            filename = 'yvih/static/member_photos/' + photo
            with open(filename, 'wb') as image:
                image.write(base64_img)
        else:
            photo = self.saveImg(
                img['src'], '{}_{}.jpg'.format(member.first_name,
                                               member.second_name), 'act'
            )
        return photo

    def getAddress(self, member):
        """All member addresses are the same so just adds genertic address"""
        address_type = AddressType.query.get(3)
        address = Address('GPO Box 1020', None, None, 'Canberra', 'ACT', 2601,
                          address_type, member, 0)
        db.session.add(address)

    def getLinks(self, td, member):
        """takes BeautifulSoup td object and loops through all the links, saving
        them as either emails or links. The links are added to the session for
        saving but not actually saved."""
        for link in td.find_all('a'):
            if link['href'].find('mailto:') > -1:
                email = Email(
                    link['href'].replace('mailto:', ''), member
                )
                db.session.add(email)
            else:
                new_link = Link(link['href'], 'website', member)
                db.session.add(new_link)

    def getPhone(self, td, member):
        """takes BeautifulSoup td object and uses regular expressions to save
        all phone numbers on the page. The phone numbers are added to the
        session for saving but not actually saved."""
        numbers = re.findall(
            r'[A-Za-z\:\ ]{3,5}\([0-9]*\)\ [0-9]*\ [0-9]*', td.text
        )
        for number in numbers:
            split_number = number.split(': ')
            if split_number[0] == 'Ph':
                num_type = 'parliamentary'
            else:
                num_type = 'parliamentary fax'
            db.session.add(
                PhoneNumber(split_number[1], num_type, member)
            )
