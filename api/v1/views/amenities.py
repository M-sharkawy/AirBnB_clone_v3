#!/usr/bin/python3
"""Create a new view for Amenity objects """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    result = []
    for i in amenities:
        result.append(i.to_dict())
    return (jsonify(result), 200)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return (jsonify(amenity.to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete specific amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_new_amenity():
    """create a new amenity"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    if "name" not in body:
        abort(400, "Missing name")

    amenity = Amenity(**body)
    storage.new(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update existing amenity by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(amenity, key, value)

    storage.save()
    return (jsonify(amenity.to_dict()), 200)
