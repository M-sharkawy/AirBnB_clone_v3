#!/usr/bin/python3
"""create a new view for City objects"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    result = []
    for i in state.cities:
        result.append(i.to_dict())
    return (jsonify(result), 200)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def cityid(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("state_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(city, key, value)

    storage.save()
    return (jsonify(city.to_dict()), 200)
