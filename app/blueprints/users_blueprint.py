from dataclasses import fields
import token
from flask import Blueprint,  request, jsonify
from marshmallow import ValidationError
import marshmallow
from webargs.flaskparser import use_args
from app import db
from app.models.users_model import User
from app.schema.users_schema import   UserSchema
from app.BL.users_bl import UserBL
from werkzeug.security import check_password_hash
from app.repo.users_repo import UserRepository  # Correct import for user repository
from app.schema.teams_schema import TeamSchema
import logging 
from webargs.flaskparser import use_kwargs


from app.utils.auth import authorize_admin  # Import the authorization middleware
from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields
from webargs.flaskparser import use_args

from app.utils.auth import authorize_roles  

# Assuming you have a User schema for serializing data




# Create a Blueprint instance for user routes
users_bp = Blueprint('users_bp', __name__)
 

#logging.basicConfig(level=logging.DEBUG)  # This ensures logging is set up properly
 
# Create User



from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.models.admin_model import Admin

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Validate admin credentials
        admin = Admin.query.filter_by(email=email).first()
        if not admin:
            return jsonify({"message": "Invalid email or password"}), 401

        # Log the stored hash and input password for debugging
        print(f"Stored Hash: {admin.password}")  # Debugging
        print(f"Input Password: {password}")  # Debugging

        # Check if password matches the stored hash
        if not check_password_hash(admin.password, password):
            return jsonify({"message": "Invalid email or password"}), 401

        # Generate JWT token with admin role
        access_token = create_access_token(identity=admin.email, additional_claims={"role": "admin"})
        
        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug: Log errors
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500



@users_bp.route('/create', methods=['POST'])
@jwt_required()  # Require valid JWT token
@use_args(UserSchema(), location="json") 
def create_user(args):  #  `args` now contains validated data
    try:
        # Fetch the current admin's email from the JWT token
        current_admin_email = get_jwt_identity()
        claims = get_jwt()
        
        # Ensure the logged-in user is an admin
        if claims.get("role") != "admin":
            return jsonify({"message": "Unauthorized. Only admins can create users."}), 403

        # Fetch the admin's ID from the `admins` table
        admin = Admin.query.filter_by(email=current_admin_email).first()
        if not admin:
            return jsonify({"message": "Admin not found in the database."}), 404

        #  Use `args` directly (already validated)
        args['admin_id'] = admin.id  

        # Create the user via BL
        response = UserBL.create_user(args, admin.id)  # Pass admin.id as the second argument
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
      

# Get All Users
@users_bp.route('/all', methods=['GET'])
#@authorize_admin
def get_all_users():

    try:
        response, status = UserBL.get_all_users()
        return jsonify(response), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



# Update User
@users_bp.route('/update', methods=['PUT'])
@jwt_required()  # Require valid JWT token
@use_args(UserSchema(), location="json") 
def update_user(args):  #   Use args directly
    try:
        print("Received Data:", args)  # Debugging

        if not args:
            return jsonify({"error": "No data received"}), 400
        
        user_id = args.get("id")
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Simulate success response
        return jsonify({"message": "User updated successfully!"}), 200

    except Exception as e:
        print("Error:", str(e))  # Log error in console
        return jsonify({"error": str(e)}), 500








# Delete User
@users_bp.route('/delete/<int:id>', methods=['DELETE'])
@authorize_roles("admin", "member", "developer")  # Multiple roles allowed
def delete_user(id):
    try:
        response, status = UserBL.delete_user(id)
        return jsonify(response), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



# # Get User by ID
# @users_bp.route('/<int:id>', methods=['GET'])
# @authorize_admin
# def get_user_by_id(id):
#     try:
#         response, status = UserBL.get_user_by_id(id)
#         return jsonify(response), status
#     except Exception as e:
#         return jsonify({"message": f"An error occurred: {str(e)}"}), 500



# @users_bp.route('/create', methods=['POST'])
# @use_args(UserSchema(), location="json")
# def create_user(data):
#     #logging.debug(f"Incoming data for user creation: {data}")
#     return UserBL.create_user(data)
