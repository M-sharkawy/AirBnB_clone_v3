#!/usr/bin/python3
"""Create a new view for Place objects """
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city_id(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    result = []
    for i in city.places:
        result.append(i.to_dict())

    return (jsonify(result), 200)


@app_views.route("places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return (jsonify(place.to_dict()), 200)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    data["city_id"] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>",  methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("city_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(place, key, value)

    storage.save()
    return (jsonify(place.to_dict()), 200)
