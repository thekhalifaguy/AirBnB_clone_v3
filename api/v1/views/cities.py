#!/usr/bin/python3
"""
Cities module to interface with the API
"""
from api.v1.views import (app_views, City, State, storage)
from flask import (request, jsonify, abort)


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def city_by_state(state_id=None):
    """
    Access the api call with on a state object to get its cities
    returns a 404 if not found.
    - POST: Creates a new city object with the state_object linked
    - GET: Default, returns all city objects linked to the state.
    """
    if state_id not in storage.all('State'):
        abort(404)

    if request.method == 'POST':
        post_obj = request.get_json()
        if post_obj is None:
            return("Not a JSON", 400)
        if 'name' not in post_obj:
            return("Missing name", 400)
        new_obj = City(**post_obj)
        new_obj.state_id = state_id
        new_obj.save()
        return(jsonify(new_obj.to_json()), 201)

    """Default: GET"""
    all_cities = storage.get('State', state_id).cities
    rtn_json = []
    for city in all_cities:
        rtn_json.append(city.to_json())
    return(jsonify(rtn_json))


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city_obj(city_id=None):
    """
    API call to interact with a specific city object
    returns a 404 if city_id is not found.
    - DELETE method: Deletes the resource and returns {}, status 200
    - PUT method: Updates the resource with the supplied json, status 201
    - GET method: Default, returns the city object
    """
    if city_id not in storage.all('City'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('City', city_id))
        storage.save()
        return(jsonify({}))

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            return("Not a JSON", 400)
        instance = storage.get('City', city_id)
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for attrib in put_obj:
            if attrib not in ignore_keys:
                setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return(jsonify(instance.to_json()))

    """ Default: GET """
    city_get = storage.get('City', city_id)
    return(jsonify(city_get.to_json()))
