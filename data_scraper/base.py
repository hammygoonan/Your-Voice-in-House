#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yvih import models, db
import os
import requests


class BaseData(object):
    """Base class for building database"""
    def __init__(self):
        if not os.path.isfile('/yvih/database.db'):
            db.create_all()
        self.createAddressTypes()
        self.createChambers()
        self.createParties()

    def createAddressTypes(self):
        """Generates all AddressTypes in the database"""
        address_types = [
            'Electoral Postal',
            'Electoral Physical',
            'Parliamentary Postal',
            'Parliamentary Physical',
            'Alternative',
            'Ministerial Postal',
            'Ministerial Physical'
        ]
        for address_type in address_types:
            atype = models.AddressType.query.\
                filter_by(address_type=address_type).first()
            if not atype:
                db.session.add(models.AddressType(address_type))
        db.session.commit()

    def createChambers(self):
        """Generates all Chambers in the database"""
        chambers = chambers = [
            {'state': 'Fed', 'house': 'House of Representatives'},
            {'state': 'Fed', 'house': 'Senate'},
            {'state': 'ACT', 'house': 'Legislative Assembly'},
            {'state': 'NSW', 'house': 'Legislative Assembly'},
            {'state': 'NSW', 'house': 'Legislative Council'},
            {'state': 'NT', 'house': 'Legislative Assembly'},
            {'state': 'Qld', 'house': 'Legislative Assembly'},
            {'state': 'SA', 'house': 'Legislative Assembly'},
            {'state': 'SA', 'house': 'House of Assembly'},
            {'state': 'Tas', 'house': 'Legislative Council'},
            {'state': 'Tas', 'house': 'House of Assembly'},
            {'state': 'Vic', 'house': 'Legislative Council'},
            {'state': 'Vic', 'house': 'Legislative Assembly'},
            {'state': 'WA', 'house': 'Legislative Assembly'},
            {'state': 'WA', 'house': 'Legislative Council'}
        ]
        for chamber in chambers:
            chamber_data = models.Chamber.query.\
                filter_by(state=chamber['state'], house=chamber['house'])\
                .first()
            if not chamber_data:
                chamber = models.Chamber(chamber['state'], chamber['house'])
                db.session.add(chamber)
        db.session.commit()

    def createParties(self):
        """ Creates a list of parties with aliases in the database"""
        parties = [
            {'name': 'Australian Labor Party', 'alias':
                ['ALP', 'Australian Labor Party (ALP)',
                 'Australian Labor Party']},
            {'name': 'Liberal Party', 'alias':
                ['LP', 'Canberra Liberals']},
            {'name': 'Australian Greens', 'alias':
                ['AG', 'ACT Greens', 'The Greens', 'Greens SA',
                 'Victorian Greens']},
            {'name': 'National Party', 'alias': ['Nats', 'The Nationals']},
            {'name': 'Liberal National Party', 'alias':
                ['Nats', 'Liberal National Party (LNP)', 'LNP']},
            {'name': 'Country Liberal Party', 'alias':
                ['CLP']},
            {'name': "Katter's Australian Party", 'alias':
                ['AUS', "Katter's Australian Party (KAP)", 'KAP']},
            {'name': 'Independent', 'alias':
                ['Ind.', 'Independent (IND)', 'IND']},
            {'name': 'Palmer United Party', 'alias':
                ['PUP']},
            {'name': 'Family First', 'alias':
                ['FFP', 'Family First Party']},
            {'name': 'Liberal Democratic Party', 'alias':
                ['LDP']},
            {'name': 'Australian Motoring Enthusiasts Party', 'alias':
                ['AMEP']},
            {'name': 'Shooters and Fishers Party', 'alias':
                ['Shooters and Fishers Party']},
            {'name': 'Christian Democratic Party (Fred Nile Group)',
             'alias': []},
            {'name': 'Dignity for Disability', 'alias': []},
            {'name': 'Democratic Labour Party', 'alias': []},
            {'name': 'Australian Sex Party', 'alias': []},
            {'name': 'Vote 1 Local Jobs', 'alias': []}
        ]
        for party in parties:
            party = models.Party(party['name'], ','.join(party['alias']))
            db.session.add(party)
        db.session.commit()

    def getParty(self, party_name):
        """Takes party name or alias and returns Party object."""
        parties = models.Party.query.all()
        for party in parties:
            if(
                party_name == party.name or
                party_name in party.alias.split(',')
            ):
                return party

    def getElectorate(self, name, chamber_id=None):
        """Returns either a preexisting electorate or a newly created electorate
        object.
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
        yvih/static/member_photos
        src, string - path to image to download
        filename, string - what to call the file
        dir, string - directory with no preceeding or trailing slash
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
