from flask import Blueprint, request, jsonify
from app.BL.users_bl import UserBL

# Create a Blueprint instance for user routes
users_bp = Blueprint('users_bp', __name__)

# Create User
@users_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()

    # Ensure required fields are provided
    if not data or not all(k in data for k in ("name", "email", "password", "role", "admin_id")):
        return jsonify({"message": "Missing required fields"}), 400

    # Delegate to UserBL for business logic
    response, status = UserBL.create_user(data)
    return jsonify(response), status

# Get All Users
@users_bp.route('/all', methods=['GET'])
def get_all_users():
    try:
        response, status = UserBL.get_all_users()
        return jsonify(response), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Get User by ID
@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        response, status = UserBL.get_user_by_id(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Update User
@users_bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        response, status = UserBL.update_user(id, data)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Delete User
@users_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        response, status = UserBL.delete_user(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
