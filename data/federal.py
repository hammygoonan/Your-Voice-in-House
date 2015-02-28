#!/usr/bin/python
import requests
from yvih import models, db
from base import BaseData
from bs4 import BeautifulSoup
import csv


class FederalData(BaseData):
    def __init__(self):
        super(FederalData, self).__init__()
        self.sen_csv = 'http://www.aph.gov.au/~/media/03%20Senators%20and%20Members/Address%20Labels%20and%20CSV%20files/allsenel.csv'

    def senate_csvs(self):
        csvfile = requests.get(self.sen_csv, stream=True)
        data = csv.DictReader(csvfile.raw)
        for row in data:
            electorate = models.Electorate.query.filter_by(name=row['State']).first()
            chamber = models.Chamber.query.get(2)
            if not electorate:
                electorate = models.Electorate(row['State'], chamber)
                db.session.add(electorate)

            party = models.Party.query.filter_by(name=row['Political Party']).first()
            if not party:
                party = models.Party(row['Political Party'])
                db.session.add(party)

            email = 'senator.' + row['Surname'].lower().replace("'", '') + '@aph.gov.au'
            member = models.Member(row['Prefered Name'], row['Surname'], row['Parliamentary Titles'], email, electorate, party)
            db.session.add(member)

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

        '''
        Need to get:
            email Address
            website
            twitter
            facebook
        '''
    def hor_csv(self):
        with open('datasets/SurnameRepsCSV.csv', 'rb') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                electorate = models.Electorate.query.filter_by(name=row['Electorate']).first()
                chamber = models.Chamber.query.get(1)
                if not electorate:
                    electorate = models.Electorate(row['Electorate'], chamber)
                    db.session.add(electorate)

                party = models.Party.query.filter_by(name=row['Political Party']).first()
                if not party:
                    party = models.Party(row['Political Party'])
                    db.session.add(party)
                if row['Preferred Name']:
                    first_name = row['Preferred Name']
                else:
                    first_name = row['First Name']

                member = models.Member(first_name, row['Surname'], row['Parliamentary Titles'], None, electorate, party)
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
                db.session.add(postal_address)
                if row['Electorate Office Fax']:
                    db.session.add(models.PhoneNumber( row['Electorate Office Fax'], 'electoral fax', member ))
                if row['Electorate Office Phone']:
                    db.session.add(models.PhoneNumber( row['Electorate Office Phone'], 'electoral phone', member ))

                db.session.commit()

            '''
            Need to get:
                email Address
                website
                twitter
                facebook
            '''


# class Scraper(object):
#     def __init__(self, url):
#         self.url = url
#         self.member_links = []
#        self.members = []
    # def getFederalMembers(self, query):
    #     page = requests.get(self.url).content
    #     soup = BeautifulSoup(page)
    #     for x in soup.find_all('p', "title"):
    #         link = x.find_all('a')
    #         if len(link) > 0 :
    #             self.member_links.append(link[0]['href'])
    #
    #     next_page = soup.find_all('a', attrs={'title' : 'Next page'})
    #     if len(next_page) > 0:
    #         getFederalMembers(next_page[0]['href'])
    #
    # def getMemberDetails(self, url):
    #     page = requests.get(url).content
    #     soup = BeautifulSoup(page)
    #     member = {}
    #     name = soup.h1.text.replace('Senator', '').replace('the Hon', '').replace('QC', '').strip().split(' ')
    #     member['first_name'] = name[0]
    #     member['second_name'] = name[1]
    #     member['electorate'] = soup.h2.text.replace('Senator for ', '').strip()
    #     summary = soup.find(id="member-summary")
    #     member['position'] = ''
    #     for position in summary.find('dl').find_all('dd')[:-2]:
    #         member['position'] += position.text + "\n"
    #     member['party'] = summary.find('dl').find_all('dd')[-2].text
    #     member['electorate'] = summary.find('dl').find_all('dd')[-1].text
    #     # print summary.find(text='Positions').next()
    #     print member



# scraper = Scraper('http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&sen=1&par=-1&gen=0&ps=0')
# scraper.getMemberDetails('http://www.aph.gov.au/Senators_and_Members/Parliamentarian?MPID=008W7')
#
#
# url = "http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results"
# queries = ["?q=&sen=1&par=-1&gen=0&ps=0", "?q=&mem=1&par=-1&gen=0&ps=0"]
