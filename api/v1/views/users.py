#!/usr/bin/python3
"""User Routes file"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve a list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieve a User object by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """Delete a User object by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new User object"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user_by_id(user_id):
    """Update an existing User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    ignored_keys = {"id", "email", "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
