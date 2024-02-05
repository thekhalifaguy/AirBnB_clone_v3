#!/usr/bin/python3
"""
Module to interface with the link between Places and Amenities
"""
from api.v1.views import (app_views, Place, Amenity, storage)
from flask import (request, jsonify, abort)


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def amenity_by_place(place_id=None):
    """
    Access the api call with on a place object to get its amenities
    returns a 404 if not found.
    - POST: Creates a new amenity object with the linked place object
    - DELETE: Default, returns all amenity objects linked to the place.
    """
    if place_id not in storage.all('Place'):
        abort(404)

    all_places = storage.get('Place', place_id).amenities
    rtn_json = []
    for place in all_places:
        rtn_json.append(place.to_json())
    return(jsonify(rtn_json))



@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def manipulate_amenties_place(place_id=None):
    """
    Access the api call with on a place object to get its amenities
    returns a 404 if not found.
    - DELETE:
    Deletes the link between Amenity objects and Place objects
    If the Amenity is not linked to the Place before the request, raise a 404 error
    Returns an empty dictionary with the status code 200
    - POST:
    Link a Amenity object to a Place
    If the Amenity is already linked to the Place, return the Amenity with the status code 200
    Returns the Amenity with the status code 201
    """
    if place_id not in storage.all('Place'):
        abort(404)

    if amenity_id not in storage.all('Amenity'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('Place', place_id))
        storage.save()
        return(jsonify({}))

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
