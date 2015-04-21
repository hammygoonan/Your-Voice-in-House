#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, jsonify, render_template, request, url_for, Blueprint, abort
from yvih import db, request_wants_json
from yvih.models import Member
from sqlalchemy.sql.expression import or_

members_blueprint = Blueprint(
    'members',
    __name__,
    template_folder='templates',
    url_prefix='/members'
)

@members_blueprint.route('/')
@members_blueprint.route('/<path:conditions>')
def members( conditions=None ):
    # if there are parameter
    if conditions != None:

        # get query and turn it into a dictionary
        conditions = conditions.split('/')
        query = list(zip(conditions[0::2], conditions[1::2]))

        # check that all fields are valid
        if not parameter_accepted(query):
            abort(400)

        # build query
        filters = []
        for conditions in query:
            if conditions[0] == 'id':
                filters.append(Member.id.in_(conditions[1].split(',')))
            else:
                for term in conditions[1].split(','):
                    filters.append(Member.__dict__[conditions[0]].ilike('%' + term + '%'))
        members = Member.query.filter( or_(*filters) )
        if members.count() == 0:
            abort(404)

    # otherwise just return the lot - may need to turn this off at some stage
    else:
        members = Member.query.all()

    # a 404 if there are no results
    if Member.query.count() == 0:
        abort(404)

    # send response
    if request_wants_json():
        results = []
        for member in members:
            results.append(member.serialise())
        return jsonify({'members' : results})
    else:
        return render_template('members.html', members=members)

def parameter_accepted(query):
    accepted = {
        'id' : int,
        'first_name' : str,
        'second_name' : str,
        'role' : str
    }
    for conditions in query:
        if conditions[0] not in accepted:
            return False
        if accepted[conditions[0]] == int and not conditions[1].isdigit():
            for member_id in conditions[1].split(','):
                if not member_id.isdigit():
                    return False
            continue # if it's an id and it has passed this test, there is no need to pass the next test
        if not isinstance(conditions[1], accepted[conditions[0]]):
            if not conditions[0] == 'id':
                return False
    return True
