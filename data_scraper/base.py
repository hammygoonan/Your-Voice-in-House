#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yvih import models, db
import os
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
        # check member is an object of Member model
        if not isinstance(address_fields.get('member'), models.Member):
            raise TypeError('Member is not a member object')
        line1 = address_fields.get('line1')
        line2 = address_fields.get('line2')
        line3 = address_fields.get('line3')
        state = address_fields.get('state')
        pcode = address_fields.get('pcode')
        suburb = address_fields.get('suburb')
        address_type = address_fields.get('address_type')
        member = address_fields.get('member')

        # check address type
        if isinstance(address_type, int):
            address_type = models.AddressType.query.get(address_type)
        if not isinstance(address_type, models.AddressType):
            raise TypeError('address_type is not an AddressType object')

        return models.Address(line1, line2, line3, suburb, state, pcode,
                              address_type, member)

    def getLink(self):
        """ return link model object
        """
        pass

    def getEmail(self):
        """ return email model object
        """
        pass

    def getPhone(self):
        """ return phone model object
        """
        pass

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

    def getElectorate(self, name, chamber_id=None):
        """ Returns either a preexisting electorate or a newly created
        electorate object.
        """
        electorate = models.Electorate.query.filter_by(name=name).first()
        if electorate:
            return electorate
        else:
            if not chamber_id:
                raise ValueError('Chamber ID not provided')
            chamber = models.Chamber.query.get(chamber_id)
            electorate = models.Electorate(name, chamber)
            db.session.add(electorate)
            db.session.commit()
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
