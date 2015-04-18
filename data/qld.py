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
        super(QldData, self).__init__()
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
        second_name = name[-1]
        if re.match('[a-z]', name[-2][0]): # if second last word starts with a lower case to account for names like 'de Brenni'
            second_name = name[-2] + ' ' + second_name
        if name[2][0] == '(': # if they have a prefered name
            first_name = name[2].replace('(', '').replace(')', '')
        else:
            first_name = name[1]

        bio = soup.find('div', 'member-bio')

        # get electorate
        left = bio.find_all('div', 'left')
        bio_p = left[1].find_all('p')

        electorate_name = bio_p[0].text.replace('Electorate', '').replace(' View Map (.pdf)', '').replace('-', '').strip()

        electorate = self.getElectorate(electorate_name, 7)
        party = self.getParty(bio_p[1].text.replace('Party', '').strip())
        job_list = bio.find('ul', 'listnoindent')
        role = job_list.text.split(':')[0]

        # images
        img_src = bio.find('img')
        img_src = img_src['src'].replace('../../../', 'https://www.parliament.qld.gov.au/')
        photo = self.saveImg(img_src, first_name + '_' + second_name + '.jpg', 'act')

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
        print re.findall(ur'\([0-9]*\)\ [0-9]*\ [0-9]*', bio.text)




        '''
        address
        phone_numbers
        '''
