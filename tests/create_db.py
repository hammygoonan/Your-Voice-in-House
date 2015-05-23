#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yvih import models, db


def create_test_db():
    db.create_all()

    # create address types
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

    # create chambers
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

    # create parties

    parties = [
        {'name': 'Australian Labor Party', 'alias':
            ['ALP', 'Australian Labor Party (ALP)',
             'Australian Labor Party']},
        {'name': 'Liberal Party', 'alias':
            ['LP', 'LIB', 'Canberra Liberals']},
        {'name': 'Australian Greens', 'alias':
            ['AG', 'ACT Greens', 'The Greens', 'Greens SA',
             'Victorian Greens', 'GWA']},
        {'name': 'National Party', 'alias':
            ['Nats', 'The Nationals', 'NAT', 'NPA']},
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
            ['Shooters and Fishers Party', 'SF']},
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

    # dummy electorate

    chamber_details = {'state': 'Fed', 'house': 'House of Representatives'}
    chamber = models.Chamber.query.filter_by(**chamber_details).first()

    # dummy members
    electorate = models.Electorate('Test Electorate', chamber)
    db.session.add(electorate)

    party = models.Party.query.filter_by(name='Australian Greens').first()
    photo = 'yvih/static/member_photos/test/test.jpg'
    member = models.Member('Hammy', 'Goonan', 'Minister for Internets',
                           electorate, party, photo)
    db.session.add(member)

    # dummy member 2
    electorate = models.Electorate('Test Electorate 2', chamber)
    db.session.add(electorate)
    party = models.Party.query.filter_by(name='Australian Labor Party').first()
    photo = 'yvih/static/member_photos/test/test2.jpg'
    member = models.Member('Gough', 'Whitlam', 'Prime Minister',
                           electorate, party, photo)
    db.session.add(member)

    db.session.commit()
