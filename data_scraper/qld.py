#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from yvih import models, db
from .base import BaseData
from bs4 import BeautifulSoup


class QldData(BaseData):
    def __init__(self):
        self.list_url = (
            'https://www.parliament.qld.gov.au/'
            'members/current/list')

    def qldData(self):
        """Loop through list of members on Website and get individual page
        links for each"""
        page = requests.get(self.list_url).content
        soup = BeautifulSoup(page)
        for thumbnail in soup.find_all('div', 'right-thumbnail'):
            link = thumbnail.find('a')
            self.memberPage('https://www.parliament.qld.gov.au' + link['href'])

    def memberPage(self, link):
        """Main processor"""
        page = requests.get(link).content
        soup = BeautifulSoup(page, "html5lib")
        name = self.getName(soup)

        bio = soup.find('div', 'member-bio')

        # get electorate
        left = bio.find_all('div', 'left')
        bio_p = left[1].find_all('p')

        electorate_name = bio_p[0].text.replace('Electorate', '').\
            replace(' View Map (.pdf)', '').replace('-', '').strip()

        electorate = self.getElectorate(electorate_name, 7)
        party = self.getParty(bio_p[1].text.replace('Party', '', 1).strip())
        job_list = bio.find('ul', 'listnoindent')
        role = job_list.text.split(':')[0]

        # images
        img_src = bio.find('img')
        img_src = img_src['src'].replace(
            '../../../',
            'https://www.parliament.qld.gov.au/'
        )
        photo = self.saveImg(
            img_src, name['first_name'] + '_' + name['second_name'] + '.jpg',
            'qld'
        )

        # create member
        member = models.Member(
            name['first_name'], name['second_name'],
            role, electorate, party, photo
        )
        db.session.add(member)

        self.processLinks(bio, member)
        self.getPhoneNumbers(bio, member)
        self.getAddresses(bio, member)

        db.session.commit()

    def getName(self, soup):
        """find page h1 and processes to return dictionary of member first_name
        and second_name"""
        name = soup.find('h1')
        name = name.text.strip().split(' ')
        # remove all the titles and 'non-name' items
        titles = ['Mr', 'Miss', 'Mrs', 'Ms', 'Hon', 'Dr', ' ', '']
        name = [n for n in name if n not in titles]
        second_name = name[-1]
        # if second last word starts
        # with a lower case to account for names like 'de Brenni'
        if re.match('[a-z]', name[-2][0]):
            second_name = name[-2] + ' ' + second_name
        # if they have a prefered name
        if name[1][0] == '(':
            first_name = name[1].replace('(', '').replace(')', '')
        else:
            first_name = name[0]
        return {'first_name': first_name, 'second_name': second_name}

    def processLinks(self, data, member):
        """takes the member detail div, loops through all the links and saves
        them as either emails or links. The links are added to the session for
        saving but not actually saved."""
        for link in data.find_all('a'):
            if link['href'].find('mailto:') > -1:
                email = models.Email(
                    link['href'].replace('mailto:', ''), member)
                db.session.add(email)
            elif(link['href'].find('javascript:DoSpeechSearch()') < 0 and
                    link['href'].find('.pdf') < 0):
                new_link = models.Link(link['href'], 'website', member)
                db.session.add(new_link)

    def getPhoneNumbers(self, data, member):
        """take member page data and uses regular expressions to save all phone
        numbers on the page. The phone numbers are added to the session for
        saving but not actually saved."""
        numbers = re.findall(
            r'[A-Za-z\:\ ]{5,7}\([0-9]*\)\ [0-9]*\ [0-9]*', data.text
        )
        for i, number in enumerate(numbers):
            split_number = number.split(': ')
            if (i > 1 and split_number[0] != 'Fax') or (i > 2):
                num_type = 'ministerial '
            else:
                num_type = 'electoral '
            db.session.add(
                models.PhoneNumber(
                    split_number[1], num_type + split_number[0].lower(),
                    member
                )
            )

    def getAddresses(self, data, member):
        """takes member page data, finds the two divs containing addresses,
        passes that data to processAddresses() and then saves the result. The
        addresses are added to the session for saving but not actually
        saved."""
        for div in ['eoAddress', 'eoPostal']:
            address = self.__processAddresses(data, div)
            if address:
                db.session.add(
                    models.Address(
                        address['address_line1'], address['address_line2'],
                        None, address['suburb'],
                        'QLD', address['postcode'],
                        address['address_type'], member, False
                    )
                )

    def __processAddresses(self, data, div):
        """processes data in div and returns dictionary of address details"""
        for i, address in enumerate(data.find_all('div', div)):
            contents = address.contents
            if len(contents) == 0:
                continue
            # get rid of header and any tag elements
            contents = [
                content for content in contents[1:]
                if isinstance(content, str)
            ]
            address_line1 = contents[0]
            address_line2 = contents[1] if len(contents) > 2 else None
            suburb = contents[-1].split(' ')[0]
            postcode = re.findall(r'[0-9]{4}', contents[-1])
            postcode = postcode[0] if len(postcode) > 0 else None
            if i > 0:
                address_type = models.AddressType.query.get(6)
            else:
                address_type = models.AddressType.query.get(2)
            return {
                'address_line1': address_line1,
                'address_line2': address_line2,
                'suburb': suburb,
                'postcode': postcode,
                'address_type': address_type
            }
