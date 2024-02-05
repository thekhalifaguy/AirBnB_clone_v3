#!/usr/bin/python3
"""
Amenitys module to interface with the API
"""
from api.v1.views import (app_views, Amenity, storage)
from flask import (request, jsonify, abort)


@app_views.route('/amenities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_amenities():
    if request.method == 'POST':
        posted_obj = request.get_json()
        if posted_obj is None:
            return("Not a JSON", 400)
        if 'name' not in posted_obj:
            return("Missing name", 400)
        new_obj = Amenity(**posted_obj)
        new_obj.save()
        return(jsonify(new_obj.to_json()), 201)

    rtn_json = []
    all_obj = storage.all('Amenity')
    for instance in all_obj:
        rtn_json.append(all_obj[instance].to_json())
    return (jsonify(rtn_json))


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_by_id(amenity_id=None):
    if amenity_id not in storage.all('Amenity'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('Amenity', amenity_id))
        storage.save()
        return(jsonify({}))

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            return("Not a JSON", 400)
        instance = storage.get('Amenity', amenity_id)
        ignore_keys = ['id', 'created_at', 'updated_at']
        for attrib in put_obj:
            if attrib not in ignore_keys:
                setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return(jsonify(instance.to_json()))

    instance = storage.get('Amenity', amenity_id)
    return(jsonify(instance.to_json()))
