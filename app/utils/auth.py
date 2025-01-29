from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

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