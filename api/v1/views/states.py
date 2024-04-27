#!/usr/bin/python3
"""State objects that handle all default RESTful API actions"""

from flask import abort, request, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states",
                 methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>",
                 methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states",
                 methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new State object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update an existing State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key in ['id', 'created_at', 'updated_at']:
        data.pop(key, None)
    for key, value in data.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
