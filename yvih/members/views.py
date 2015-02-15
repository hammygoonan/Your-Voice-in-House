from flask import redirect, render_template, request, url_for, Blueprint
from yvih import db   # pragma: no cover
from yvih.models import Member

members_blueprint = Blueprint(
    'members', __name__,
    template_folder='templates'
)

@members_blueprint.route('/', methods=['GET'])
def members( conditions=None ):
    # @todo: add conditions
    if conditions != None:
        conditions = conditions.split('/')
        query = dict(zip(conditions[0::2], conditions[1::2]))
        # @todo validate query
        members = Member.query.filter_by( **query )
    else:
        members = Member.query.all()
    if request_wants_json():
        results = []
        for member in members:
            results.append(member.serialise())
        return jsonify({'members' : results})
    else:
        return render_template('members.html', members=members)

def request_wants_json():
    # taken from http://flask.pocoo.org/snippets/45/
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
