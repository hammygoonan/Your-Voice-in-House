#!/usr/bin/python
from flask import Flask, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)
app.debug = True
#app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

####################
# Global functions #
####################

def request_wants_json():
    # taken from http://flask.pocoo.org/snippets/45/
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

#####################
# Import Blueprints #
#####################

from yvih.home.views import home_blueprint
from yvih.members.views import members_blueprint
from yvih.electorates.views import electorates_blueprint
from yvih.chambers.views import chambers_blueprint

# register our blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(members_blueprint)
app.register_blueprint(electorates_blueprint)
app.register_blueprint(chambers_blueprint)

##################
# Error Handling #
##################

# Page not found
@app.errorhandler(404)
def page_not_found(e):
    if request_wants_json():
        return jsonify({ 'error' : 'Either you have requested a page that does not exist or your query has returned no results.'}), 404
    else:
        return render_template('404.html'), 404

# unsupported method
@app.errorhandler(405)
def page_not_found(e):
    if request_wants_json():
        return jsonify({ 'error' : 'Method not supported. You should probably be using a get request'}), 405
    else:
        return render_template('405.html'), 405
