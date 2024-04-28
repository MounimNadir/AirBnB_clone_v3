#!/usr/bin/python3
"""State objects that handle all default RESTful API actions"""

from flask import abort, request, jsonify
from models import storage
from models.state import State
from api.v1.views import app_views

# Define constants for error messages
ERROR_JSON_NOT_FOUND = "No JSON data found"
ERROR_MISSING_NAME = "Name field is missing"
ERROR_STATE_NOT_FOUND = "State not found"


@app_views.route("/states", methods=["GET"],
                 strict_slashes=False)
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
        abort(404, ERROR_STATE_NOT_FOUND)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, ERROR_STATE_NOT_FOUND)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states",
                 methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new State object"""
    data = request.get_json()
    if not data:
        abort(400, ERROR_JSON_NOT_FOUND)
    if "name" not in data or not data["name"]:
        abort(400, ERROR_MISSING_NAME)
    new_state = State(name=data["name"])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update an existing State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, ERROR_STATE_NOT_FOUND)
    data = request.get_json()
    if not data:
        abort(400, ERROR_JSON_NOT_FOUND)
    # Define which fields can be updated
    allowed_fields = ["name"]
    for key, value in data.items():
        if key in allowed_fields:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
