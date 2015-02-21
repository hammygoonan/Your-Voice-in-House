from flask import redirect, jsonify, render_template, request, url_for, Blueprint, abort
from yvih import db, request_wants_json
from yvih.models import Member

members_blueprint = Blueprint(
    'members',
    __name__,
    template_folder='templates',
    url_prefix='/members'
)

@members_blueprint.route('/')
@members_blueprint.route('/<path:conditions>')
def members( conditions=None ):
    # @todo: add conditions
    if conditions != None:
        conditions = conditions.split('/')
        query = dict(zip(conditions[0::2], conditions[1::2]))
        if not peramiter_accepted(query):
            abort(404)

        members = Member.query.filter_by( **query )
        # 404 if no results
        if members.count() == 0:
            abort(404)
    else:
        members = Member.query.all()

    if request_wants_json():
        results = []
        for member in members:
            results.append(member.serialise())
        return jsonify({'members' : results})
    else:
        return render_template('members.html', members=members)

def peramiter_accepted(query):
    # if there was an uneven number of paramiters
    if not isinstance(query, dict):
        return False

    accepted = {
        'id' : int,
        'first_name' : unicode,
        'second_name' : unicode,
        'role' : unicode
    }
    for field, value in query.iteritems():
        if field not in accepted:
            return False
        if accepted[field] == int and value.isdigit():
            continue
        if not isinstance(value, accepted[field]):
            return False
    return True
