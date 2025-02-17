#!/usr/bin/python3
'''
app views fo airbnb
'''
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=["GET"])
def get_data():
    '''returns status'''
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=["GET"])
def count_():
    '''retrieves the number of each objects by type'''
    total = {}
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }

    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count

    return jsonify(total)
