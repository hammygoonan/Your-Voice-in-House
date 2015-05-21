#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
from io import StringIO


class FileManager(object):
    def getPage(self, url):
        """ Returns content from url as string """
        response = self.__getFile(url)
        return response.content

    def getExcel(self, url):
        """ Returns dictionary of CSV Data """
        # csvfile = requests.get(url, stream=True)
        # temp_file = 'temp.xls'
        # with open(temp_file, 'wb') as f:
        #     for chunk in csvfile.iter_content():
        #         f.write(chunk)
        # f.close()
        # book = xlrd.open_workbook(temp_file)
        # sheet_names = book.sheet_names()
        # sheet = book.sheet_by_name(sheet_names[0])
        # # header = sheet.row_values(0)
        # values = []
        # for rownum in range(1, sheet.nrows):
        #     values.append(
        #         # dict(zip(header, sheet.row_values(rownum)))
        #         sheet.row_values(rownum)
        #     )
        # os.remove(temp_file)
        # return values
        pass

    def getCsv(self, url):
        """ returns content of csv file as dictionary """
        response = self.__getFile(url, True)
        return self.dictReader(response.text)

    def dictReader(self, file):
        return csv.DictReader(StringIO(file))

    def __getFile(self, url, stream_flag=False):
        """ returns page as a stream """
        response = requests.get(url, stream=stream_flag)
        if response.status_code == 200:
            return response
        else:
            raise Exception(url + ' status code: ' + str(response.status_code))
