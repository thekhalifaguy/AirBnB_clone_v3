#!/usr/bin/python3
"""
Users module to interface with the API
"""
from api.v1.views import (app_views, User, storage)
from flask import (request, jsonify, abort)


@app_views.route('/users',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_users():
    """
    Adds new User objects, if provided with a name parameter in a POST request
    Default is to Returns a list of all users in json format for GET requests
    """
    all_users = storage.all('User')
    if request.method == 'POST':
        posted_obj = request.get_json()
        if posted_obj is None:
            return("Not a JSON", 400)
        if 'email' not in posted_obj.keys():
            return("Missing email", 400)
        if 'password' not in posted_obj.keys():
            return("Missing password", 400)
        # linear search through users to see if email is in db already
        for user in all_users:
            email_in_db = getattr(all_users.get(user), 'email')
            if posted_obj['email'] == email_in_db:
                return("ERROR: Email is already registered", 400)
        new_obj = User(**posted_obj)
        new_obj.save()
        return(jsonify(new_obj.to_json()), 201)

    rtn_json = []
    for instance in all_users:
        rtn_json.append(all_users[instance].to_json())
    return (jsonify(rtn_json))


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_by_id(user_id=None):
    """
    Access the api call with on a specific user object
    returns a 404 if not found.
    Delete method removes the object
    Defaults is to return the user object.
    """
    if user_id not in storage.all('User'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('User', user_id))
        storage.save()
        return(jsonify({}))

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            return("Not a JSON", 400)
        instance = storage.get('User', user_id)
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for attrib in put_obj:
            if attrib not in ignore_keys:
                setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return(jsonify(instance.to_json()))

    """Default: GET request returns the object in json form"""
    instance = storage.get('User', user_id)
    return(jsonify(instance.to_json()))
