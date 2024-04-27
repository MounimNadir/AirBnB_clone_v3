#!/usr/bin/python3
"""User objects that handle all default RESTful API actions"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def users(user_id=None):
    """Show users and users with specific ID"""
    users_list = []
    if user_id is None:
        all_objs = storage.all(User).values()
        for v in all_objs:
            users_list.append(v.to_dict())
        return jsonify(users_list)
    else:
        result = storage.get(User, user_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def users_delete(user_id):
    """Delete User object by ID"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_users():
    """Create a new User object via POST request"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_users(user_id):
    """Update User object"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
