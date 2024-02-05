#!/usr/bin/python3
"""
landing page for api
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def app_status():
    """
    Simply returns the state of the api.
    """
    return(jsonify(status="OK"))


@app_views.route('/stats')
def app_get_count():
    """
    Returns statistics about the number of objects available
    """
    tojson = {}
    for cls in storage.available_classes:
        string = str(cls).lower()
        if string[-1] is 'y':
            string = string[0:-1] + "ies"
        else:
            string += "s"
        tojson.update({string: storage.count(cls)})
    return(jsonify(tojson))
