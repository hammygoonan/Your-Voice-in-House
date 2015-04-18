#!/usr/bin/python
from yvih import db

class Electorate(db.Model):
    __tablename__ = "electorates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chambers.id'))
    members = db.relationship('Member')

    chamber = db.relationship('Chamber', backref=db.backref('chambers', lazy='dynamic'))

    def __init__(self, name, chamber):
        self.name = name
        self.chamber = chamber

    def serialise(self):
        data = {
            'id' : self.id,
            'name' : self.name,
            'state' : self.chamber.state,
            'house' : self.chamber.house,
            'members' : []
        }
        for member in self.members:
            data['members'].append({
                'id' : member.id,
                'first_name' : member.first_name,
                'second_name' : member.second_name,
                'role' : member.role,
                'party' : member.party.name
            })
        return data

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    role = db.Column(db.Text)
    email = db.Column(db.String)
    electorate_id = db.Column(db.Integer, db.ForeignKey('electorates.id'))
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    electorate = db.relationship('Electorate', backref=db.backref('electorates', lazy='dynamic'))
    party = db.relationship('Party', backref=db.backref('parties', lazy='dynamic'))
    photo = db.Column(db.Text)

    email = db.relationship('Email')
    addresses = db.relationship('Address')
    phone_numbers = db.relationship('PhoneNumber')
    links = db.relationship('Link')

    def __init__(self, first_name, second_name, role, electorate, party, photo):
        self.first_name = first_name
        self.second_name = second_name
        self.role = role
        self.electorate = electorate
        self.party = party
        self.photo = photo

    def serialise(self):
        data = {
            'id' : self.id,
            'first_name' : self.first_name,
            'second_name' : self.second_name,
            'role' : self.role,
            'email' : self.email,
            'electorate' : { 'id' : self.electorate.id, 'name' : self.electorate.name, 'state' : self.electorate.chamber.state, 'house' : self.electorate.chamber.house },
            'party' : { 'name' : self.party.name },
            'addresses' : [],
            'phone_numbers' : [],
            'links' : []

        }
        for address in self.addresses:
            data['addresses'].append({
                'address_line1' : address.address_line1,
                'address_line2' : address.address_line2,
                'address_line3' : address.address_line3,
                'suburb' : address.suburb,
                'state' : address.state,
                'postcode' : address.postcode,
                'address_type' : address.address_type.address_type
            })
        for phone_number in self.phone_numbers:
            data['phone_numbers'].append({
                'number' : phone_number.number,
                'type' : phone_number.type
            })
        for link in self.links:
            data['links'].append({
                'link' : link.link,
                'type' : link.type,
            })
        data['links'].append({
            'self' : '/members/id/' + str(data['id'])
        })
        return data

class Party(db.Model):
    __tablename__ = "parties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    alias = db.Column(db.Text)

    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    member = db.relationship('Member')

    def __init__(self, email, member):
        self.email = email
        self.member = member

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

class PhoneNumber(db.Model):
    '''
        Phone number types: parliamentary, electoral, tollfree, fax, electoral fax, parliamentary fax, ministerial phone, ministerial fax
    '''
    __tablename__ = "phone_numbers"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    type = db.Column(db.String)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    member = db.relationship('Member')

    def __init__(self, number, type, member):
        self.number = number
        self.type = type
        self.member = member

class Link(db.Model):
    '''
        Link types: website, wikipedia, twitter
    '''
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    type = db.Column(db.String)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    member = db.relationship('Member')

    def __init__(self, link, type, member):
        self.link = link
        self.type = type
        self.member = member

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
        self.address_type = address_type

class Chamber(db.Model):
    '''
        1|House of Representatives|Fed
        2|Senate|Fed
    '''
    __tablename__ = "chambers"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)
    house = db.Column(db.String)
    electorates = db.relationship('Electorate')

    def __init__(self, state, house):
        self.state = state
        self.house = house

    def serialise(self):
        data = {
            'id' : self.id,
            'state' : self.state,
            'house' : self.house,
            'electorates' : []
        }
        for electorate in self.electorates:
            data['electorates'].append({
                'id' : electorate.id,
                'name' : electorate.name,
            })
        return data

class Tags(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.Text)

    def __init__(self, name, data):
        self.name = name
        self.data = data
