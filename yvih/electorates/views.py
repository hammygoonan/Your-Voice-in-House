from flask import redirect, render_template, request, url_for, Blueprint
from yvih import db   # pragma: no cover
from yvih.models import Electorate

electorates_blueprint = Blueprint(
    'electorates', __name__,
    template_folder='templates'
)

@electorates_blueprint.route('/electorates/<path:conditions>', methods=['GET'])
def electorates( conditions=None ):
    # add query
    # add template
    # add if json
    electorates = Electorate.query.all()
    results = []
    for electorate in electorates:
        results.append( electorate.serialise() )
    return jsonify({'electorates' : results})
