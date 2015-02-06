import app
import models
from scrapers import federal
import os

if not os.path.isfile('database.db'):
    app.db.create_all()

def create_address_types( address_types ):
    for address_type in address_types:
        atype = models.AddressType.query.filter_by( address_type=address_type ).first()
        if not atype:
            app.db.session.add( models.AddressType( address_type ) )
    app.db.session.commit()

def create_chambers( chambers ):
    for chamber in chambers:
        chamber_data = models.Chamber.query.filter_by( state=chamber['state'], house=chamber['house'] ).first()
        if not chamber_data:
            app.db.session.add( models.Chamber( chamber['state'], chamber['house']) )
    app.db.session.commit()

address_types =['Electoral Postal', 'Electoral Physical', 'Parliamentary Postal', 'Parliamentary Physical', 'Alternative']
create_address_types( address_types )

chambers = [
    {'state' : 'Fed', 'house' : 'House of Representatives'},
    {'state' : 'Fed', 'house' : 'Senate'}
]
create_chambers( chambers )

federal.fed_csvs()
