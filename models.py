#!/usr/bin/python
from app import db

class Electorate(db.Model):
    __tablename__ = "electorates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chambers.id'))

    chamber = db.relationship('Chamber', backref=db.backref('chambers', lazy='dynamic'))

    def __init__(self, name, chamber):
        self.name = name
        self.chamber = chamber

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    role = db.Column(db.Text)
    electorate_id = db.Column(db.Integer, db.ForeignKey('electorates.id'))
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))

    electorate = db.relationship('Electorate', backref=db.backref('electorates', lazy='dynamic'))
    party = db.relationship('Party', backref=db.backref('parties', lazy='dynamic'))
    address = db.relationship('Address')

    def __init__(self, first_name, second_name, role, electorate, party):
        self.first_name = first_name
        self.second_name = second_name
        self.role = role
        self.electorate = electorate
        self.party = party

class Party(db.Model):
    __tablename__ = "parties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    address_line1 = db.Column(db.String)
    address_line2 = db.Column(db.String)
    address_line3 = db.Column(db.String)
    suburb = db.Column(db.String)
    state = db.Column(db.String)
    postcode = db.Column(db.String)
    address_type_id = db.Column(db.Integer, db.ForeignKey('address_types.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    primary = db.Column(db.Boolean)

    address_type = db.relationship('AddressType', backref=db.backref('address_types', lazy='dynamic'))
    member = db.relationship('Member', backref=db.backref('members', lazy='dynamic'))

    def __init__(self, address_line1, address_line2, address_line3, suburb, state, postcode, address_type, member, primary):
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.suburb = suburb
        self.state = state
        self.postcode = postcode
        self.address_type = address_type
        self.member = member
        self.primary = primary

class AddressType(db.Model):
    '''
        1|Electoral Postal
        2|Electoral Physical
        3|Parliamentary Postal
        4|Parliamentary Physical
        5|Alternative
    '''
    __tablename__ = 'address_types'

    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.String)

    def __init__(self, address_type):
        self.type = address_type

class Chamber(db.Model):
    '''
        1|House of Representatives|Fed
    '''
    __tablename__ = "chambers"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)
    house = db.Column(db.String)

    def __init__(self, state, house):
        self.state = state
        self.house = house

class Tags(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name
