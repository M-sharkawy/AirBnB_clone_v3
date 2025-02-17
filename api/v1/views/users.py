#!/usr/bin/python3
"""users Routes file"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_list():
    '''
    return list for all User objects
    '''
    usr_list = []
    users = storage.all(User)
    for user in users.values():
        usr_list.append(user.to_dict())
    return jsonify(usr_list)


@app_views.route("/places/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_usr_id(user_id):
    '''
    return user object by id
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_obj(user_id):
    '''
    delete user obj according to id
    '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def update_userlist():
    '''
    Create user list
    '''
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city(user_id):
    """Updates a User object"""
    city = storage.get(User, user_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    data.pop("id", None)
    data.pop("state_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    for key, value in data.items():
        setattr(city, key, value)

    storage.save()
    return (jsonify(city.to_dict()), 200)

