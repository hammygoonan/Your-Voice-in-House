from flask import redirect, render_template, request, url_for, Blueprint
from yvih import db   # pragma: no cover
from yvih.models import Chamber

chambers_blueprint = Blueprint(
    'chambers', __name__,
    template_folder='templates'
)

@chambers_blueprint.route('/chambers', methods=['GET'])
def chambers():
    chambers = Chamber.query.all()
    results = []
    for chamber in chambers:
        results.append( chamber.serialise() )
    return jsonify({'chamber' : results})
