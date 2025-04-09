from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from app.models.admin_model import Admin   
from app.models.users_model import User 
# Ensure you import the Admin model

from app import db


def authorize_admin(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        # Extract the user identity from the JWT token (which should include the role)
        current_user = get_jwt_identity()
        
        # Debug: print current_user to check its type and structure
        print("Current User:", current_user)
        
        # Check if current_user is a dictionary and contains the role
        if isinstance(current_user, dict) and "role" in current_user:
            if current_user["role"] != "Admin":
                return jsonify({"message": "Unauthorized, admin privileges required."}), 403
        else:
            return jsonify({"message": "Invalid user data."}), 400
        
        return fn(*args, **kwargs)

    return wrapper


from werkzeug.security import check_password_hash
def authorize_roles(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data or "email" not in data or "password" not in data:
                return jsonify({"message": "Missing authentication details"}), 400

            email = data["email"]
            password = data["password"]

            # Fetch user from users table
            user = User.query.filter_by(email=email).first()

            if not user:
                return jsonify({"message": "Invalid credentials."}), 401

            # Ensure password is verified
            if not check_password_hash(user.password, password):
                return jsonify({"message": "Invalid credentials."}), 401

            print(f"  User Found: {user}")
            print(f"  User Role: {user.role}")

            # Check if user role is authorized
            if user.role.lower() in [r.lower() for r in allowed_roles]:
                return fn(*args, **kwargs)

            return jsonify({"message": "Unauthorized, insufficient privileges."}), 403

        return wrapper
    return decorator