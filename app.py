#!/usr/bin/python
from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

import models

@app.route("/")
def hello():
    member = models.Member.query.all()
    print member
    return "Hello World!"

@app.route('/members', methods=['GET'])
def members():
    if request.args:
        query = request.args.to_dict()
        members = models.Member.query.filter_by( **query )
    else:
        members = models.Member.query.all()
    results = []
    for member in members:
        results.append(member.serialise())
    return jsonify({'members' : results})

@app.route('/member')
def member():
    pass


if __name__ == "__main__":
    app.run()
