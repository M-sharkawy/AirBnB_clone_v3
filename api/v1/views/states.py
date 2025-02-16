#!/usr/bin/python3
"""States Routes file"""
from api.v1.views import app_views
import sys
import os
from models.state import State
from flask import jsonify, abort, request


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")))

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all States"""
    from models import storage
    states = storage.all(State).values()
    return (jsonify([state.to_dict() for state in states]))


@app_views.route("/states/<state_id>", methods=["GET"],
                 strict_slashes=False)
def get_states_with_id(state_id):
    """Retrieves a State object"""
    from models import storage
    state = storage.get(State, state_id)
    if state:
        return (jsonify(state.to_dict()))
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def remove_state(state_id):
    """Deletes a State object"""
    from models import storage
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_new_state():
    """Creates a State"""
    from models import storage
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return (jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """Updates a State object"""
    from models import storage
    state_data = storage.get(State, state_id)
    if not state_data:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    body.pop("id", None)
    body.pop("created_at", None)
    body.pop("updated_at", None)
    for key, value in body.items():
        setattr(state_data, key, value)
    storage.save()

    return (jsonify(state_data.to_dict()), 200)
