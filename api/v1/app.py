#!/usr/bin/python3
'''
AirBnB_clone_v3 API constructor
'''
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(self):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def notfounderror(error):
    '''handle error message'''
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
