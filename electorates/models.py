from django.db import models


class House(models.Model):
	name = models.CharField(max_length=255)
	duristriction = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name


class Electorate(models.Model):
	name = models.CharField(max_length=255)
	house = models.ForeignKey(House)
	def __unicode__(self):
		return self.name

class Party(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=5)
	def __unicode__(self):
		return self.name

class Member(models.Model):
	first_name = models.CharField(max_length=255)
	second_name = models.CharField(max_length=255)
	electorate = models.ForeignKey(Electorate)
	job = models.TextField()
	party = models.ForeignKey(Party)
	twitter = models.CharField(max_length=255)
	website = models.CharField(max_length=255)
	def __unicode__(self):
		return self.first_name + ' ' + self.second_name
		
class AddressType(models.Model):
	address_type = models.CharField(max_length=255)
	def __unicode__(self):
		return self.address_type
		
class Address(models.Model):
	address = models.TextField()
	member = models.ForeignKey(Member)
	address_type = models.ForeignKey(AddressType)
	def __unicode__(self):
		return self.address

class Email(models.Model):
	email = models.CharField(max_length=255)
	member = models.ForeignKey(Member)
	def __unicode__(self):
		return self.email