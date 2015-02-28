from yvih import app, models, db
import os

class BaseData(object):
    '''Base class for building database'''
    def __init__(self):
        if not os.path.isfile('database.db'):
            db.create_all()
        self.address_types = ['Electoral Postal', 'Electoral Physical', 'Parliamentary Postal', 'Parliamentary Physical', 'Alternative']
        self.chambers = [
            {'state' : 'Fed', 'house' : 'House of Representatives'},
            {'state' : 'Fed', 'house' : 'Senate'},
            {'state' : 'ACT', 'house' : 'Legislative Assembly'},
            {'state' : 'NSW', 'house' : 'Legislative Assembly'},
            {'state' : 'NSW', 'house' : 'Legislative Council'},
            {'state' : 'NT', 'house' : 'Legislative Assembly'},
            {'state' : 'Qld', 'house' : 'Legislative Assembly'},
            {'state' : 'SA', 'house' : 'Legislative Assembly'},
            {'state' : 'SA', 'house' : 'House of Assembly'},
            {'state' : 'Tas', 'house' : 'Legislative Council'},
            {'state' : 'Tas', 'house' : 'House of Assembly'},
            {'state' : 'Vic', 'house' : 'Legislative Council'},
            {'state' : 'Vic', 'house' : 'Legislative Assembly'},
            {'state' : 'WA', 'house' : 'Legislative Assembly'},
            {'state' : 'WA', 'house' : 'Legislative Council'}
        ]
        self.create_address_types()
        self.create_chambers()

    def create_address_types( self ):
        for address_type in self.address_types:
            atype = models.AddressType.query.filter_by( address_type=address_type ).first()
            if not atype:
                db.session.add( models.AddressType( address_type ) )
        db.session.commit()

    def create_chambers( self ):
        for chamber in self.chambers:
            chamber_data = models.Chamber.query.filter_by( state=chamber['state'], house=chamber['house'] ).first()
            if not chamber_data:
                db.session.add( models.Chamber( chamber['state'], chamber['house']) )
        db.session.commit()
