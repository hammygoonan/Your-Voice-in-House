#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import csv
from app import db
import models

with open('datasets/allsenstate.csv', 'rb') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        electorate = models.Electorate(row['State'], 1)
        party = models.Party(row['Political Party'])
        member = models.Member(row['Prefered Name'], row['Surname'], row['Parliamentary Titles'], electorate, party)
        db.session.add(electorate)
        db.session.add(party)
        db.session.add(member)
        db.session.commit()


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
