from flask import Blueprint, request, jsonify
from .models import add_user, get_users

bp = Blueprint("api", __name__)

@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    add_user(data)
    return jsonify({"message": "User added successfully"}), 201

@bp.route("/users", methods=["GET"])
def fetch_users():
    users = get_users()
    return jsonify(users), 200
