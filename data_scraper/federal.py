#!/usr/bin/python
import requests
from urllib import quote
from yvih import models, db
from base import BaseData
from bs4 import BeautifulSoup
import csv


class FederalData(BaseData):
    def __init__(self):
        self.sen_csv = 'http://www.aph.gov.au/~/media/03%20Senators%20and%20Members/Address%20Labels%20and%20CSV%20files/allsenel.csv'
        self.hor_csv = 'http://www.aph.gov.au/~/media/03%20Senators%20and%20Members/Address%20Labels%20and%20CSV%20files/SurnameRepsCSV.csv'

    def updateSenate(self):
        data = self.getCsvData(self.sen_csv)
        for row in data:
            member = models.Member.query.join(models.Electorate)\
                        .filter(models.Electorate.chamber_id == 2)\
                        .filter(models.Member.second_name == row['Surname'])\
                        .filter(models.Member.first_name == row['Prefered Name'])\
                        .first()
            if member == None:
                issue = '%s %s was found in Senate csv but not in database.' % (row['Prefered Name'], row['Surname'])
                db.session.add(
                    models.Data('cron', 'cron@yourvoiceinhouse.org.au', issue, None)
                )
                continue

            # check party
            if self.getParty(row['Political Party']) != member.party:
                issue = '%s %s seems to have changed political party.' % (row['Prefered Name'], row['Surname'])
                db.session.add(
                    models.Data('cron', 'cron@yourvoiceinhouse.org.au', issue, member.id)
                )

            # check electorate
            if self.getElectorate(row['State']) != member.electorate:
                issue = '%s %s seems to have changed electorate.' % (row['Prefered Name'], row['Surname'])
                db.session.add(
                    models.Data('cron', 'cron@yourvoiceinhouse.org.au', issue, member.id)
                )

            # Addresses
            # Phone Numbers
            # Images
            # Links
            # Email


        db.session.commit()
    def generateSenate(self):
        data = self.getCsvData(self.sen_csv)
        for row in data:
            electorate = self.getElectorate(row['State'], 2)

            party = self.getParty(row['Political Party'])

            member = models.Member(row['Prefered Name'], row['Surname'], row['Parliamentary Titles'], electorate, party, None)
            db.session.add(member)

            email = models.Email('senator.' + row['Surname'].lower().replace("'", '') + '@aph.gov.au', member)
            db.session.add(email)

            address_type = models.AddressType.query.get(2)
            electoratal_address = models.Address(
                row['Electorate AddressLine1'],
                row['Electorate AddressLine2'],
                None,
                row['Electorate Suburb'],
                row['Electorate State'],
                row['Electorate Postcode'],
                address_type,
                member,
                False
            )
            db.session.add(electoratal_address)

            address_type = models.AddressType.query.get(1)
            postal_address = models.Address(
                row['Label Address'],
                None,
                None,
                row['Label Suburb'],
                row['Label State'],
                row['Label Postcode'],
                address_type,
                member,
                False
            )
            address_type = models.AddressType.query.get(3)
            postal_address = models.Address(
                'The Senate, Parliament House',
                None,
                None,
                'Canberra',
                'ACT',
                '2600',
                address_type,
                member,
                False
            )
            db.session.add(postal_address)
            if row['Electorate Fax']:
                db.session.add(models.PhoneNumber( row['Electorate Fax'], 'electoral fax', member ))
            if row['Electorate Telephone']:
                db.session.add(models.PhoneNumber( row['Electorate Telephone'], 'electoral phone', member ))
            if row['Electorate Toll Free']:
                db.session.add(models.PhoneNumber( row['Electorate Toll Free'], 'electoral tollfree', member ))

            db.session.commit()
            self.scrapePage(member, 'sen')

    def horCsvs(self):
        #csvfile = requests.get(self.hor_csv, stream=True)
        #data = csv.DictReader(csvfile.raw)
        file = open('SurnameRepsCSV.csv')
        data = csv.DictReader(file)
        for row in data:
            electorate = self.getElectorate(row['Electorate'], 1)

            party = self.getParty(row['Political Party'])

            if row['Preferred Name']:
                first_name = row['Preferred Name']
            else:
                first_name = row['First Name']

            member = models.Member(first_name, row['Surname'], row['Parliamentary Titles'], electorate, party, None)
            db.session.add(member)

            address_type = models.AddressType.query.get(2)
            electoratal_address = models.Address(
                row['Electorate Office Postal Address'],
                None,
                None,
                row['Electorate Office Postal Suburb'],
                row['Electorate Office Postal State'],
                row['Electorate Office Postal PostCode'],
                address_type,
                member,
                False
            )
            db.session.add(electoratal_address)
            if row['Electorate Office Fax']:
                db.session.add(models.PhoneNumber( row['Electorate Office Fax'], 'electoral fax', member ))
            if row['Electorate Office Phone']:
                db.session.add(models.PhoneNumber( row['Electorate Office Phone'], 'electoral phone', member ))

            db.session.commit()
            self.scrapePage(member, 'mem')

    def scrapePage(self, member, house):
        '''
            house can be either 'sen' or 'mem'
        '''
        # search for member
        query_string = quote(member.first_name + '+' + member.second_name)

        # @todo check response code
        page = requests.get("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?expand=1&q=" + query_string + "&" + house + "=1&par=-1&gen=0&ps=10").content
        soup = BeautifulSoup(page)

        # find link to member page in first search result

        ul = soup.find('ul', 'search-filter-results')
        if ul == None:
            issue = '%s %s was found found in CSV file but not in a serach of the APH website.' % (row['Prefered Name'], row['Surname'])
            db.session.add(
                models.Data('cron', 'cron@yourvoiceinhouse.org.au', issue, None)
            )
            return None

        member_url = ul.find('a')['href']
        member_page = requests.get("http://www.aph.gov.au/" + member_url).content

        # go to member page
        soup = BeautifulSoup(member_page)

        # get image and save as base64 string
        thumbnail = soup.find('p', 'thumbnail')
        if thumbnail:
            image = thumbnail.find('img')
            photo = self.saveImg(image['src'], member.first_name + '_' + member.second_name + '.jpg', 'fed')
            member.photo = photo

        # get all the links in the second div with a class of 'box'
        box = soup.find_all('div', 'box')[1]
        links = box.find_all('a')

        # tidy up the links
        for link in links:
            if link['href'].find('mailto:') == 0:
                email = models.Email(link['href'].replace('mailto:', ''), member)
                db.session.add(email)
            else:
                if link.text != 'Contact form':
                    if link.text == 'Twitter':
                        link_type = 'twitter'
                    elif link.text == 'Facebook':
                        link_type = 'facebook'
                    else:
                        link_type = 'website'
                    if link['href'][0] == '/':
                        href = "http://www.aph.gov.au" + link['href']
                    else:
                        href = link['href']
                    new_link = models.Link(href, link_type, member)
                    db.session.add(new_link)
        db.session.commit()

    def getCsvData(self, file):
        ''' Returns dictionary of CSV Data '''
        csvfile = requests.get(file, stream=True)
        return csv.DictReader(csvfile.raw)
