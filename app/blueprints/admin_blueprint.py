from flask import Blueprint, request, jsonify
from app.BL.admin_bl import AdminBL
from app.repo.admin_repo import AdminRepository
from app.schema.admin_schema import AdminSchema

# Create a Blueprint instance for admin routes
admin_bp = Blueprint('admin_bp', __name__)
admin_schema = AdminSchema()
admin_list_schema = AdminSchema(many=True)

# Test route
@admin_bp.route('/', methods=['GET'])
def index():
    return "Admin Blueprint Works!"

# Create Admin
@admin_bp.route('/create', methods=['POST'])
def create_admin():
    try:
        data = request.get_json()
        result, status = AdminBL.create_admin(**data)
        return jsonify(admin_schema.dump(result) if status == 201 else result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Get All Admins
@admin_bp.route('/all', methods=['GET'])
def get_all_admins():
    try:
        admins = AdminRepository.get_all_admins()
        return jsonify(admin_list_schema.dump(admins)), 200
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

# Update Admin
@admin_bp.route('/update/<int:id>', methods=['PUT'])
def update_admin(id):
    try:
        data = request.get_json()
        result, status = AdminBL.update_admin(admin_id=id, **data)
        return jsonify(admin_schema.dump(result) if status == 200 else result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Delete Admin
@admin_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_admin(id):
    try:
        result, status = AdminBL.delete_admin(id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
    