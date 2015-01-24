from app import db

class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    role = db.Column(db.String)
    electorate_id = db.Column(db.Integer, db.ForeignKey('electorate.id'))

    def __init__(self, first_name, second_name, role, electorate_id):
        self.first_name = first_name
        self.second_name = second_name
        self.role = role
        self.electorate_id = electorate_id

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
    primary = db.Column(db.Boolean)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

class AddressType(db.Model):
    __tablename__ = 'address_types'
    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.String)

    def __init__(self, address_type):
        self.type = address_type

class Electorate(db.Model):
    __tablename__ = "electorates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    chamber_id = db.Column(db.Integer, db.ForeignKey('chambers.id'))
    def __init__(self, name, chamber_id):
        self.name = name
        self.chamber_id = chamber_id

class Chamber(db.Model):
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
