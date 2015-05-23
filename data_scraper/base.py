#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yvih import models, db
import os
import re
import requests


class BaseData(object):
    """Base class for building database"""
    def __init__(self):
        pass

    def getName(self, *names):
        """ returns dictionary of first_name and second_name
        """
        if len(names) != 2:
            raise ValueError('Name must be a list or tuple with 2 elements')
        return {'first_name': names[0], 'second_name': names[1]}

    def getRole(self, role):
        """ return a string of member role
        """
        if not isinstance(role, str):
            raise TypeError('Role needs to be a string')
        return role

    def getAddress(self, **address_fields):
        """ return address model object
        """
        # check keys
        required_keys = ['line1', 'state', 'pcode', 'suburb', 'member',
                         'address_type']
        address_keys = address_fields.keys()
        for required_key in required_keys:
            if required_key not in address_keys:
                raise KeyError('{} key is missing from addresses'
                               .format(required_key))

        line1 = address_fields.get('line1')
        line2 = address_fields.get('line2')
        line3 = address_fields.get('line3')
        state = address_fields.get('state')
        pcode = address_fields.get('pcode')
        suburb = address_fields.get('suburb')
        address_type = address_fields.get('address_type')
        member = address_fields.get('member')

        self.isMember(member)
        # check address type
        if isinstance(address_type, int):
            address_type = models.AddressType.query.get(address_type)
        if not isinstance(address_type, models.AddressType):
            raise TypeError('address_type is not an AddressType object')

        return models.Address(line1, line2, line3, suburb, state, pcode,
                              address_type, member)

    def getLink(self, link, link_type, member):
        """ return link model object
        """
        # check link
        if not isinstance(link, str):
            raise ValueError('{} is not a string'.format(link))
        if link[0:4] != 'http':
            raise ValueError('{} does not start with http'.format(link))
        # check link type
        link_types = ['facebook', 'twitter', 'wikipedia', 'website']
        if link_type not in link_types:
            raise ValueError('{} is not a valid link type'.format(link_type))
        self.isMember(member)
        return models.Link(link, link_type, member)

    def getEmail(self, email, member):
        """ return email model object
        """
        if not re.match('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)', email):
            raise ValueError('{} is not a vaild email address'.format(email))
        self.isMember(member)
        return models.Email(email, member)

    def getPhoneNumber(self, number, number_type, member):
        """ return phone model object
        """
        if not isinstance(number, str):
            raise ValueError('Phone number must be a string')
        self.isMember(member)
        valid_types = ['parliamentary', 'electoral', 'tollfree', 'fax',
                       'electoral fax', 'parliamentary fax',
                       'ministerial', 'ministerial fax', 'alternative',
                       'alternative fax']
        if number_type not in valid_types:
            raise ValueError('{} is not a valid number type'.
                             format(number_type))
        return models.PhoneNumber(number, number_type, member)

    def getParty(self, party_name):
        """ Takes party name or alias and returns Party object.
        """
        parties = models.Party.query.all()
        for party in parties:
            if(
                party_name == party.name or
                party_name in party.alias.split(',')
            ):
                return party
        raise ValueError('{} is not a party name or alias'.format(party_name))

    def getElectorate(self, name, chamber):
        """ Returns either a preexisting electorate or a newly created
        electorate object.
        """
        if isinstance(chamber, int):
            chamber = models.Chamber.query.get(chamber)
            if not chamber:
                raise ValueError('{} is an invalid chamber id'.format(chamber))
        elif not isinstance(chamber, models.Chamber):
            raise ValueError('{} chamber must be an integer or Chamber model'
                             'object'.format(chamber))
        electorate = models.Electorate.query.filter_by(
            name=name, chamber_id=chamber.id
        ).first()
        if electorate:
            return electorate
        else:
            electorate = models.Electorate(name, chamber)
            return electorate

    def saveImg(self, src, filename, dir=""):
        """saves a file and returns the file page relateive to
        yvih/static/member_photos src, string - path to image to download
        filename, string - what to call the file dir, string - directory with
        no preceeding or trailing slash
        """
        imgfile = requests.get(src)
        static = 'yvih/static/member_photos/'
        if not dir[-1] == '/':
            directory = dir + '/'
        if not os.path.isdir(static + directory):
            os.makedirs(static + directory)
        with open(static + directory + filename, 'wb') as photo:
            photo.write(imgfile.content)
        return directory + filename

    def isMember(self, member):
        if not isinstance(member, models.Member):
            raise TypeError('Member is not a member object')
