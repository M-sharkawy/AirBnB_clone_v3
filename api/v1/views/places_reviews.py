#!/usr/bin/python3
"""API routes for handling Review objects"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews_by_placeid(place_id):
    """Retrieve all Review objects of a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieve a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review_by_id(review_id):
    """Delete a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review_by_placeid(place_id):
    """Create a new Review for a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")

    data["place_id"] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review_by_id(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    ignored_keys = {"id", "user_id", "place_id", "created_at", "updated_at"}
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
