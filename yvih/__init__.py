#!/usr/bin/python
from flask import Flask, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from yvih.home.views import home_blueprint
from yvih.members.views import members_blueprint
from yvih.electorates.views import electorates_blueprint
from yvih.chambers.views import chambers_blueprint

# register our blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(members_blueprint)
app.register_blueprint(electorates_blueprint)
app.register_blueprint(chambers_blueprint)

def request_wants_json():
    # taken from http://flask.pocoo.org/snippets/45/
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
