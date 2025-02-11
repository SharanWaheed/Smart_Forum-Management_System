from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from app.BL.admin_bl import AdminBL
from app.models.admin_model import Admin
from app.schema.admin_schema import AdminSchema
from app.repo.admin_repo import AdminRepository
from app.schema.admin_schema import AdminSchema
from webargs.flaskparser import use_args
from flask import Blueprint, request, jsonify
from app.utils.auth import authorize_admin  # Import middleware
from app.repo.admin_repo import AdminRepository

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route("/create", methods=["POST"])
@use_args(AdminSchema(), location="json")  
def create_admin(args):
    admin = AdminRepository.create_admin(**args)   
    return jsonify({"message": "Admin created successfully!"}), 201



@admin_blueprint.route('/view-teams', methods=['GET'])
@authorize_admin
def view_teams():
    # Example logic for fetching teams
    return jsonify({"teams": []}), 200

 
admin_bp = Blueprint('admin_bp', __name__)

admin_schema = AdminSchema()
admin_list_schema = AdminSchema(many=True)

# Test route
@admin_bp.route('/', methods=['GET'])
def index():
    return "Admin Blueprint Works!"

# Create Admin
# In admin_blueprint.py (Route File)
@admin_bp.route('/create', methods=['POST'])
@use_args(AdminSchema(), location="json")
def create_admin(args):
    try:
        # If validation passes, process the data
        result, status = AdminBL.create_admin(**args)
        
        # Return the serialized admin object
        return jsonify(result), status
    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@admin_bp.route('/all', methods=['GET'])
def get_all_admins():
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Fetch admins with users eagerly loaded
        admins_query = AdminRepository.get_all_admins_with_users(page=page, per_page=per_page)

        # Serialize the admin data
        admins_data = [admin.serialize() for admin in admins_query]

        # Return response with pagination data
        return jsonify({
            "admins": admins_data,
            "current_page": page,
            "total_pages": len(admins_query) // per_page + (1 if len(admins_query) % per_page > 0 else 0),
            "total_records": len(admins_query)
        }), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


# Update Admin
@admin_bp.route('/update', methods=['PUT'])
@use_args(AdminSchema(), location="json_or_form")
def update_admin(args):  
    try:
        print("  Parsed Data:", args)  # Debugging step

        admin_id = args.get("id")
        if not admin_id:
            return jsonify({"error": "Admin ID is required"}), 400

        result, status = AdminBL.update_admin(admin_id=admin_id, **args)

        if status != 200:
            return jsonify(result), status  # If error, return it properly

        return jsonify(AdminSchema().dump(result)), status

    except Exception as e:
        print("  Unexpected Error:", str(e))  
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



# Delete Admin
@admin_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_admin(id):
    try:
        result, status = AdminBL.delete_admin(id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
    
    
# Get Admin by ID
@admin_bp.route('/<int:id>', methods=['GET'])

def get_admin_by_id(id):
    try:
        result, status = AdminBL.get_admin_by_id(id)
        return jsonify(admin_schema.dump(result) if status == 200 else result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    