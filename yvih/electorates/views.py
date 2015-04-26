#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, Blueprint
from yvih.models import Electorate

electorates_blueprint = Blueprint(
    'electorates',
    __name__,
    template_folder='templates',
    url_prefix='/electorates'
)


@electorates_blueprint.route('/')
@electorates_blueprint.route('/<path:conditions>')
def electorates(conditions=None):
    # add query
    # add template
    # add if json
    electorates = Electorate.query.all()
    results = []
    for electorate in electorates:
        results.append(electorate.serialise())
    return jsonify({'electorates': results})
