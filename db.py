#!/usr/bin/env python

import pymysql
from electorate import Electorate

class db:
	def __init__(self):
		self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='yvih', unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock"	)
		self.cur = self.conn.cursor()
	def get_electorates(self):
		electoral_data = []
		self.cur.execute("SELECT * FROM electorates")
		for row in self.cur.fetchall():
			electoral_data.append(row)
		return electoral_data
		
	def get_members(self):
		member_data = []
		self.cur.execute("SELECT * FROM members")
		for row in cur.fetchall() :
			member_data.append(row)
		return memberl_data
		
x = db()
electorate_data = x.get_electorates()
electorates = []
for row in electorate_data:
	electorates.append(Electorate(row))

print electorates[1].name