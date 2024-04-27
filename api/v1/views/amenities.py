#!/usr/bin/python3
"""Amenity objects that handle all default RESTful API actions"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET"])
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["GET"])
def amenities(amenity_id=None):
    """Show amenities and amenities with specific ID"""
    amenities_list = []
    if amenity_id is None:
        all_objs = storage.all(Amenity).values()
        for v in all_objs:
            amenities_list.append(v.to_dict())
        return jsonify(amenities_list)
    else:
        result = storage.get(Amenity, amenity_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def amenities_delete(amenity_id):
    """Delete Amenity object by ID"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities",
                 strict_slashes=False, methods=["POST"])
def create_amenities():
    """Create a new Amenity object via POST request"""
    data = request.get_json(force=True,
                            silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["PUT"])
def update_amenities(amenity_id):
    """Update Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True,
                            silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
