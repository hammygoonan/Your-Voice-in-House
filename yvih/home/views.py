from flask import redirect, render_template, request, url_for, Blueprint

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

@home_blueprint.route("/")
def api():
    return render_template('api.html')
