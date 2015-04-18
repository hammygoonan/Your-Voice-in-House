#!/usr/bin/python
import requests
import base64
import re
from urllib import quote
from yvih import models, db
from base import BaseData
from bs4 import BeautifulSoup
import csv


class QldData(BaseData):
    def __init__(self):
        self.list_url = 'https://www.parliament.qld.gov.au/members/current/list'

    def qldData(self):
        page = requests.get(self.list_url).content
        soup = BeautifulSoup(page)
        for thumbnail in  soup.find_all('div', 'right-thumbnail'):
            link = thumbnail.find('a');
            self.memberPage('https://www.parliament.qld.gov.au' + link['href'])
    def memberPage(self, link):
        page = requests.get(link).content
        soup = BeautifulSoup(page, "html5lib")
        name = soup.find('h1')
        name = name.text.strip().split(' ')
        # remove all the titles and 'non-name' items
        titles = ['Mr', 'Miss', 'Mrs', 'Ms', 'Hon', 'Dr', ' ', '']
        name = [n for n in name if n not in titles]
        second_name = name[-1]
        if re.match('[a-z]', name[-2][0]): # if second last word starts with a lower case to account for names like 'de Brenni'
            second_name = name[-2] + ' ' + second_name
        if name[1][0] == '(': # if they have a prefered name
            first_name = name[1].replace('(', '').replace(')', '')
        else:
            first_name = name[0]

        bio = soup.find('div', 'member-bio')

        # get electorate
        left = bio.find_all('div', 'left')
        bio_p = left[1].find_all('p')

        electorate_name = bio_p[0].text.replace('Electorate', '').replace(' View Map (.pdf)', '').replace('-', '').strip()

        electorate = self.getElectorate(electorate_name, 7)
        party = self.getParty(bio_p[1].text.replace('Party', '', 1).strip())
        job_list = bio.find('ul', 'listnoindent')
        role = job_list.text.split(':')[0]

        # images
        img_src = bio.find('img')
        img_src = img_src['src'].replace('../../../', 'https://www.parliament.qld.gov.au/')
        photo = self.saveImg(img_src, first_name + '_' + second_name + '.jpg', 'qld')

        # create member
        member = models.Member(first_name, second_name, role, electorate, party, photo)
        db.session.add(member)

        # emails and links
        for link in bio.find_all('a'):
            if link['href'].find('mailto:') > -1:
                email = models.Email(link['href'].replace('mailto:', ''), member)
                db.session.add(email)
            elif link['href'].find('javascript:DoSpeechSearch()') < 0 and link['href'].find('.pdf') < 0:
                new_link = models.Link(link['href'], 'website', member)
                db.session.add(new_link)

        # phone numbers
        numbers = re.findall(ur'[A-Za-z\:\ ]{5,7}\([0-9]*\)\ [0-9]*\ [0-9]*', bio.text)
        for i, number in enumerate(numbers):
            split_number = number.split(': ')
            if (i > 1 and split_number[0] != 'Fax') or (i > 2):
                num_type = 'ministerial '
            else:
                num_type = 'electoral '
            db.session.add(
                models.PhoneNumber(split_number[1], num_type + split_number[0].lower(), member)
            )

        # address
        for i, eo_address in enumerate(bio.find_all('div', 'eoAddress')):
            contents = eo_address.contents
            if len(contents) == 0:
                continue
            # get rid of header and any tag elements
            contents = [content for content in contents[1:] if isinstance(content, unicode)]
            address_line1 = contents[0]
            address_line2 = contents[1] if len(contents) > 2 else None
            suburb = contents[-1].split(' ')[0]
            postcode = re.findall(ur'[0-9]{4}', contents[-1])
            postcode = postcode[0] if len(postcode) > 0 else None
            if i > 0:
                address_type = models.AddressType.query.get(6)
            else:
                address_type = models.AddressType.query.get(2)

            db.session.add(
                models.Address(address_line1, address_line2, None, suburb, 'QLD', postcode, address_type, member, False)
            )
        for i, eo_postal in enumerate(bio.find_all('div', 'eoPostal')):
            contents = eo_postal.contents
            if len(contents) == 0:
                continue
            # get rid of header and any tag elements
            contents = [content for content in contents[1:] if isinstance(content, unicode)]
            address_line1 = contents[0]
            address_line2 = contents[1] if len(contents) > 2 else None
            suburb = contents[-1].split(' ')[0]
            postcode = re.findall(ur'[0-9]{4}', contents[-1])
            postcode = postcode[0] if len(postcode) > 0 else None
            if i > 0:
                address_type = models.AddressType.query.get(6)
            else:
                address_type = models.AddressType.query.get(2)

            db.session.add(
                models.Address(address_line1, address_line2, None, suburb, 'QLD', postcode, address_type, member, False)
            )

        db.session.commit()
