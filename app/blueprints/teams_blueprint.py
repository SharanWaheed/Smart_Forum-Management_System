from flask import Blueprint, request, jsonify
from app.BL.teams_bl import TeamBL
from webargs.flaskparser import use_args

from app.schema.teams_schema import TeamSchema



teams_bp = Blueprint('teams_bp', __name__)

# Test Route
@teams_bp.route("/", methods=["GET"])
def index():
    return "Teams Blueprint Works!"

# Create Team
@teams_bp.route("/create", methods=["POST"])
@use_args(TeamSchema(), location="json")
def create_team(args):
 
#     data = request.get_json()
#     name = data.get('name')
#     description = data.get('description', '')
#     admin_id = data.get('admin_id')

#     result, status = TeamBL.create_team(name, description, admin_id)
#     return jsonify(result), status
    name = args.get('name')
    description = args.get('description', '')
    admin_id = args.get('admin_id')

    result, status = TeamBL.create_team(name, description, admin_id)
    return jsonify(result), status

# Get All Teams
@teams_bp.route("/all", methods=["GET"])
def get_all_teams():
    result = TeamBL.get_all_teams()
    return jsonify(result), 200

# Get Team by ID
@teams_bp.route("/<int:id>", methods=["GET"])
def get_team_by_id(id):
    result, status = TeamBL.get_team_by_id(id)
    return jsonify(result), status

# Update Team

@teams_bp.route("/update/<int:id>", methods=["PUT"])
#@use_args(TeamSchema(), location="json")
def update_team(id):
    data = request.get_json()
    result, status = TeamBL.update_team(id, **data)
    return jsonify(result), status

# Delete Team
@teams_bp.route('/delete/<int:team_id>', methods=['DELETE'])
def delete_team(team_id): 
    result, status = TeamBL.delete_team(team_id)
    return jsonify(result), status

# Add User to Team
@teams_bp.route("/<int:team_id>/add_user", methods=["POST"])
def add_user_to_team(team_id):
    data = request.get_json()
    user_id = data.get("user_id")
    
    result, status = TeamBL.add_user_to_team(team_id, user_id)
    return jsonify(result), status

# Remove User from Team
@teams_bp.route("/<int:team_id>/remove_user", methods=["DELETE"])
def remove_user_from_team(team_id):
    data = request.get_json()
    user_id = data.get("user_id")
    
    result, status = TeamBL.remove_user_from_team(team_id, user_id)
    return jsonify(result), status

# Get All Users in a Team
@teams_bp.route("/<int:team_id>/users", methods=["GET"])
def get_users_in_team(team_id):
    result, status = TeamBL.get_users_in_team(team_id)
    return jsonify(result), status
    