#!/usr/bin/python3
"""Cities objects that handles all default RESTFul API actions"""

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


@app_views.route("cities/<city_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def city_delete(city_id):
    """delete method"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def create_city():
    """create a new post req"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """update city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
