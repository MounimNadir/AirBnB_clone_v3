#!/usr/bin/python3
"""Cities objects that handle all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["GET"])
def get_cities_by_state(state_id=None):
    """Retrieve list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=["GET"])
def get_city(city_id=None):
    """Retrieve a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=["DELETE"])
def city_delete(city_id):
    """Delete method"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """Create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
