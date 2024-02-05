#!/usr/bin/python3
"""
Module to interface with the link between Places and Amenities
"""
from api.v1.views import (app_views, Place, Review, storage)
from flask import (request, jsonify, abort)

#from api.v1.views import get_linked


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def review_by_place(place_id=None):
    """
    Access the api call with on a place object to get its reviews
    returns a 404 if not found.
    - POST: Creates a new review object with the place_object linked
    - GET: Default, returns all review objects linked to the place.
    """
    if place_id not in storage.all('Place'):
        abort(404)

    if request.method == 'POST':
        posted_obj = request.get_json()
        if posted_obj is None:
            return("Not a JSON", 400)
        if 'name' not in posted_obj:
            return("Missing name", 400)
        new_obj = State(**posted_obj)
        storage.save()
        return(jsonify(new_obj.to_json()), 201)

#    all_reviews = storage.get('Place', place_id).review
#    rtn_json = []
#    for review in all_reviews:
#        rtn_json.append(review.to_json())
    return(get_linked('Place', place_id, review))



@app_views.route('reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_reviews(review_id=None):
    """
    Access the api call with on a place object to get its reviews
    returns a 404 if not found.
    - GET: Default, gets a review at <review_id>, status 200
    - DELETE: Deletes the review at id. Returns '{}', status 200
    - PUT:
    """
    if review_id not in storage.all('Review'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('Review', review_id))
        storage.save()
        return(jsonify({}))

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            return("Not a JSON", 400)
        instance = storage.get('Review', review_id)
        ignore_keys = ['id', 'user_id', 'place_id', 'updated_at']
        for attrib in put_obj:
            if attrib not in ignore_keys:
                setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return(jsonify(instance.to_json()))

    """ Default: GET """
    instance_get = storage.get('Review', review_id)
    return(jsonify(instance_get.to_json()))
