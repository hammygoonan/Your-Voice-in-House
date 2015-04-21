#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, jsonify, render_template, request, url_for, Blueprint
from yvih import db
from yvih.models import Chamber

chambers_blueprint = Blueprint(
    'chambers',
    __name__,
    template_folder='templates',
    url_prefix='/chambers'
)

@chambers_blueprint.route('/')
@chambers_blueprint.route('/<path:conditions>')
def chambers():
    chambers = Chamber.query.all()
    results = []
    for chamber in chambers:
        results.append( chamber.serialise() )
    return jsonify({'chamber' : results})
