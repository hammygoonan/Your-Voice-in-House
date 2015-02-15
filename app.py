#!/usr/bin/python
from flask import Flask, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

import models

@app.route("/")
def api():
    return render_template('api.html')

@app.route('/members/<path:conditions>', methods=['GET'])
def members( conditions=None ):
    if conditions != None:
        conditions = conditions.split('/')
        query = dict(zip(conditions[0::2], conditions[1::2]))
        # @todo validate query
        members = models.Member.query.filter_by( **query )
    else:
        members = models.Member.query.all()
    if request_wants_json():
        results = []
        for member in members:
            results.append(member.serialise())
        return jsonify({'members' : results})
    else:
        return render_template('members.html', members=members)

@app.route('/electorates/<path:conditions>', methods=['GET'])
def electorates( conditions=None ):
    # add query
    # add template
    # add if json
    electorates = models.Electorate.query.all()
    results = []
    for electorate in electorates:
        results.append( electorate.serialise() )
    return jsonify({'electorates' : results})

@app.route('/chambers', methods=['GET'])
def chambers():
    chambers = models.Chamber.query.all()
    results = []
    for chamber in chambers:
        results.append( chamber.serialise() )
    return jsonify({'chamber' : results})

def request_wants_json():
    # taken from http://flask.pocoo.org/snippets/45/
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

if __name__ == "__main__":
    app.run()
