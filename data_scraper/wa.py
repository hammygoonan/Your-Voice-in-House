#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BaseData
import requests
import os
import xlrd
from yvih import models


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
            # 'assembly': {
            #     'csv': 'http://www.parliament.wa.gov.au/WebCMS/WebCMS.nsf/re' +
            #            'sources/file-mla-merge-data/$file/MLA%20Merge%20Data' +
            #            '%2020150205.xls',
            #     'site': 'http://www.parliament.wa.gov.au/parliament/memblist' +
            #             '.nsf/WAssemblyMembers?openform'
            # }
        }

    def waData(self):
        for house, urls in self.houses.items():
            data = self.getData(urls['csv'])
            if house == 'council':
                self.getCouncilMembers(data)
            else:
                self.getAssemblyMembers(data)

    def getCouncilMembers(self, data):
        for row in data:
            party = self.getParty(row['PARTY'])
            electorate = self.getElectorate(row['REGION'], 15)
            role = self.getRole(
                row['OTHER_POSITIONS HELD'], row['MINISTERIAL_POSITIONS']
            )

            photo = self.getPhoto()
            member = models.Member(row['PREFERRED_NAME'], row['SURNAME'],
                                   role, electorate, party, photo)
            print(member.__dict__)

    def getAssemblyMembers(self, data):
        pass

    def getRole(self, ministerial, other):
        if ministerial and not other:
            return ministerial
        if other and ministerial:
            return '{}\n{}'.format(other, ministerial)
        if other and not ministerial:
            return other
        return None

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
        header = sheet.row_values(0)
        values = []
        for rownum in range(1, sheet.nrows):
            values.append(
                dict(zip(header, sheet.row_values(rownum)))
            )
        os.remove(temp_file)
        return values

    def getPhoto(self):
        return None
