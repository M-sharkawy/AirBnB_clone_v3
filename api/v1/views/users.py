#!/usr/bin/python3
"""handles all RESTFul API actions for User objects"""
from api.v1.views import app_views
from models import storage
from models.user import User
import hashlib
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return (jsonify([obj.to_dict() for obj in users]))


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return (jsonify(user.to_dict()))


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def del_user_by_id(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")

    m = hashlib.md5(str.encode(data["password"]))
    data["password"] = m.hexdigest()

    user = User(**data)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update existing user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("email", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    if "password" in data:
        m = hashlib.md5(str.encode(data["password"]))
        data["password"] = m.hexdigest()

    for key, value in data.items():
        setattr(user, key, value)

    storage.save()
    return (jsonify(user.to_dict()), 200)
