#!/usr/bin/env python

class Member:
	def __init__(self, data):
		self.first_name = data.first_name
		self.second_name = data.second_name
		self.emails = data.emails
		self.addresses = data.addresses
		self.phone_numbers = data.phone_numbers
		self.website = data.website
		self.twitter = data.twitter
	def add_electorate(self, electorate):
		pass