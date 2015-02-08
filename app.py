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

@app.route('/members', methods=['GET'])
def members():
    if request.args:
        query = request.args.to_dict()
        members = models.Member.query.filter_by( **query )
    else:
        members = models.Member.query.all()
    # query = {'name' : 'Melbourne'}
    # members = models.Member.query.join(models.Electorate).filter_by( **query )
    if request.accept_mimetypes.accept_json:
        results = []
        for member in members:
            results.append(member.serialise())
        return jsonify({'members' : results})
    else:
        return render_template('members.html', members=members)

@app.route('/electorates', methods=['GET'])
def electorates():
    electorates = models.Electorate.query.all()
    results = []
    for electorate in electorates:
        results.append( electorate.serialise() )
    return jsonify({'electorates' : results})


if __name__ == "__main__":
    app.run()
