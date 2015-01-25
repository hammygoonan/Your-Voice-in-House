#!/usr/bin/python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

import models

@app.route("/")
def hello():
    member = models.Member
    return "Hello World!"

if __name__ == "__main__":
    app.run()
