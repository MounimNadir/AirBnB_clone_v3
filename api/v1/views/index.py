#!/usr/bin/python3
"""define routes of blueprint
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status",
                 strict_slashes=False, methods=["GET"])
def api_status():
    """Return status."""
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route("/stats",
                 strict_slashes=False, methods=["GET"])
def stats():
    """Return statistics."""
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)

    response = {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users,
    }

    return jsonify(response)
