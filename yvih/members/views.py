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

    # if there are parameiters
    if conditions != None:

        # get query and turn it into a dictionary
        conditions = conditions.split('/')
        query = zip(conditions[0::2], conditions[1::2])

        # check that all fields are valid
        if not peramiter_accepted(query):
            abort(400)

        # build query
        filters = []
        for conditions in query:
            if conditions[0] == 'id':
                filters.append(Member.id.is_(conditions[1]))
            else:
                filters.append(Member.__dict__[conditions[0]].ilike('%' + conditions[1] + '%'))
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

def peramiter_accepted(query):
    accepted = {
        'id' : int,
        'first_name' : unicode,
        'second_name' : unicode,
        'role' : unicode
    }
    for conditions in query:
        if conditions[0] not in accepted:
            return False
        if accepted[conditions[0]] == int and conditions[1].isdigit():
            continue
        if not isinstance(conditions[1], accepted[conditions[0]]):
            return False
    return True
