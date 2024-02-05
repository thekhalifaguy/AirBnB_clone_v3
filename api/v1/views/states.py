#!/usr/bin/python3
"""
States module to interface with the API
"""
from api.v1.views import (app_views, State, storage)
from flask import (request, jsonify, abort)


@app_views.route('/states',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_states():
    """
    Access the api call on all state objects
    - POST: Adds a new State object. Requires name parameter.
    - GET: Default, returns a list of all states
    """
    if request.method == 'POST':
        posted_obj = request.get_json()
        if posted_obj is None:
            return("Not a JSON", 400)
        if 'name' not in posted_obj:
            return("Missing name", 400)
        new_obj = State(**posted_obj)
        storage.save()
        return(jsonify(new_obj.to_json()), 201)

    """ Default: GET"""
    rtn_json = []
    all_obj = storage.all('State')
    for instance in all_obj:
        rtn_json.append(all_obj[instance].to_json())
    return (jsonify(rtn_json))


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_by_id(state_id=None):
    """
    Access the api call with on a specific state object
    returns a 404 if not found.
    - DELETE: Removes the state object
    - PUT: Updates the state object
    - GET: Default, return the state object.
    """
    if state_id not in storage.all('State'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('State', state_id))
        storage.save()
        return(jsonify({}))

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            return("Not a JSON", 400)
        instance = storage.get('State', state_id)
        for attrib in put_obj:
            setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return(jsonify(instance.to_json()))

    """ Default: GET"""
    instance = storage.get('State', state_id)
    return(jsonify(instance.to_json()))
